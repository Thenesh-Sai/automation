using Microsoft.Extensions.DependencyInjection;
using Microsoft.Playwright;
using NUnit.Framework;
using Siloverse.Configuration;
using Siloverse.Configuration.Dependencies;
using Siloverse.Infrastructure.Dependencies;
using Siloverse.UI.Dependencies;

namespace Siloverse.Tests.UI.Base;

public abstract class UiTestBase
{
    protected ServiceProvider RootServices { get; private set; } = null!;
    protected TestSettings Settings { get; private set; } = null!;
    protected IPlaywright PlaywrightInstance { get; private set; } = null!;
    protected IBrowser Browser { get; private set; } = null!;
    protected IBrowserContext Context { get; private set; } = null!;
    protected IPage Page { get; set; } = null!;
    protected string ArtifactsRoot { get; private set; } = string.Empty;

    [SetUp]
    public async Task UiSetUpAsync()
    {
        var collection = new ServiceCollection();
        collection.AddSiloverseConfiguration(Environment.GetEnvironmentVariable("SILOVERSE_TEST_ENV") ?? "Test");
        collection.AddSiloverseInfrastructure();
        RootServices = collection.BuildServiceProvider();
        Settings = RootServices.GetRequiredService<TestSettings>();

        ArtifactsRoot = Path.Combine(
            TestContext.CurrentContext.WorkDirectory,
            Settings.ArtifactsDirectory,
            Sanitize(TestContext.CurrentContext.Test.Name));
        Directory.CreateDirectory(ArtifactsRoot);

        PlaywrightInstance = await Playwright.CreateAsync();
        Browser = await PlaywrightInstance.Chromium.LaunchAsync(new BrowserTypeLaunchOptions
        {
            Headless = Settings.Browser.Headless,
            SlowMo = Settings.Browser.SlowMoMs
        });

        Context = await Browser.NewContextAsync(new BrowserNewContextOptions
        {
            IgnoreHTTPSErrors = true,
            ViewportSize = new ViewportSize { Width = 1440, Height = 900 }
        });
        Context.SetDefaultTimeout(Settings.Browser.TimeoutMs);

        if (Settings.Browser.TraceOnFailure)
        {
            await Context.Tracing.StartAsync(new TracingStartOptions
            {
                Screenshots = true,
                Snapshots = true,
                Sources = true
            });
        }

        Page = await Context.NewPageAsync();
    }

    [TearDown]
    public async Task UiTearDownAsync()
    {
        var failed = TestContext.CurrentContext.Result.Outcome.Status == NUnit.Framework.Interfaces.TestStatus.Failed;

        try
        {
            if (failed && Settings.Browser.ScreenshotOnFailure && Page is not null)
            {
                await Page.ScreenshotAsync(new PageScreenshotOptions
                {
                    Path = Path.Combine(ArtifactsRoot, "failure.png"),
                    FullPage = true
                });
            }

            if (Context is not null && Settings.Browser.TraceOnFailure)
            {
                await Context.Tracing.StopAsync(new TracingStopOptions
                {
                    Path = failed ? Path.Combine(ArtifactsRoot, "trace.zip") : null
                });
            }
        }
        finally
        {
            if (Context is not null)
            {
                await Context.CloseAsync();
            }

            if (Browser is not null)
            {
                await Browser.CloseAsync();
            }

            PlaywrightInstance?.Dispose();
            if (RootServices is not null)
            {
                await RootServices.DisposeAsync();
            }
        }
    }

    protected T GetPage<T>() where T : notnull
    {
        var collection = new ServiceCollection();
        collection.AddSiloverseConfiguration(Environment.GetEnvironmentVariable("SILOVERSE_TEST_ENV") ?? "Test");
        collection.AddSiloverseInfrastructure();
        collection.AddSiloverseUi();
        collection.AddSingleton(Page);
        collection.AddLogging();
        var sp = collection.BuildServiceProvider();
        return sp.GetRequiredService<T>();
    }

    protected void RequireCredentials()
    {
        if (string.IsNullOrWhiteSpace(Settings.Credentials.Username) ||
            string.IsNullOrWhiteSpace(Settings.Credentials.Password))
        {
            Assert.Ignore("Set SILOVERSE_USERNAME and SILOVERSE_PASSWORD to run authenticated UI tests.");
        }
    }

    protected async Task SignInViaIdentityAsync()
    {
        RequireCredentials();
        var login = GetPage<Siloverse.UI.Pages.Shared.LoginPage>();
        await login.OpenAsync();
        await login.SignInAsync(Settings.Credentials.Username, Settings.Credentials.Password);
        await Page.WaitForURLAsync("**/launchpoint-ui.dev.siloverse.space/**", new PageWaitForURLOptions
        {
            Timeout = Settings.Browser.TimeoutMs
        });
    }

    protected async Task LaunchAvrWorkspaceAsync(string matterNumber)
    {
        var workspaces = GetPage<Siloverse.UI.Pages.LaunchPoint.AvrWorkspacesPage>();
        await workspaces.OpenAsync();
        await workspaces.SearchAsync(matterNumber);
        await workspaces.OpenWorkspaceRowAsync(matterNumber);

        var popupTask = Context.WaitForPageAsync(new BrowserContextWaitForPageOptions
        {
            Timeout = Settings.Browser.TimeoutMs
        });
        await workspaces.ConfirmLaunchWorkspaceAsync();

        IPage avrPage;
        try
        {
            avrPage = await popupTask;
        }
        catch (TimeoutException)
        {
            avrPage = Context.Pages.LastOrDefault(p => p.Url.Contains("avr.dev.siloverse.space", StringComparison.OrdinalIgnoreCase))
                      ?? Page;
            if (!avrPage.Url.Contains("avr.dev.siloverse.space", StringComparison.OrdinalIgnoreCase))
            {
                await avrPage.WaitForURLAsync("**/avr.dev.siloverse.space/**", new PageWaitForURLOptions
                {
                    Timeout = Settings.Browser.TimeoutMs
                });
            }
        }

        await avrPage.BringToFrontAsync();
        await avrPage.WaitForLoadStateAsync(LoadState.DOMContentLoaded);

        // Wide viewports keep the Modules sidebar open (no hamburger); narrow view uses it.
        var dashboardReady = avrPage.GetByRole(AriaRole.Heading, new() { Name = "Review Summary" })
            .Or(avrPage.GetByRole(AriaRole.Navigation, new() { Name = "Modules" })
                .GetByRole(AriaRole.Button, new() { Name = "Dashboard" }))
            .Or(avrPage.GetByRole(AriaRole.Button, new() { Name = "Open module navigation" }));

        await dashboardReady.First.WaitForAsync(new LocatorWaitForOptions
        {
            State = WaitForSelectorState.Visible,
            Timeout = Settings.Browser.TimeoutMs
        });
        Page = avrPage;
    }

    private static string Sanitize(string name)
        => string.Join("_", name.Split(Path.GetInvalidFileNameChars()));
}
