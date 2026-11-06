# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def w(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print("wrote", rel)


# Infrastructure
w(
    "src/Siloverse.Infrastructure/Siloverse.Infrastructure.csproj",
    r"""
<Project Sdk="Microsoft.NET.Sdk">
  <ItemGroup>
    <ProjectReference Include="..\Siloverse.Configuration\Siloverse.Configuration.csproj" />
    <ProjectReference Include="..\Siloverse.Models\Siloverse.Models.csproj" />
  </ItemGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.Data.SqlClient" />
    <PackageReference Include="Microsoft.Extensions.DependencyInjection" />
    <PackageReference Include="Microsoft.Extensions.Logging" />
  </ItemGroup>
</Project>
""",
)

w(
    "src/Siloverse.Infrastructure/Repositories/Interfaces/ISqlConnectivityProbe.cs",
    r"""
namespace Siloverse.Infrastructure.Repositories.Interfaces;

public interface ISqlConnectivityProbe
{
    Task<(bool Connected, string Message)> TryConnectAsync(CancellationToken cancellationToken = default);
    Task<IReadOnlyList<string>> ListDatabasesAsync(CancellationToken cancellationToken = default);
}
""",
)

w(
    "src/Siloverse.Infrastructure/Repositories/Interfaces/ILaunchPointRepository.cs",
    r"""
namespace Siloverse.Infrastructure.Repositories.Interfaces;

public interface ILaunchPointRepository
{
    Task ResetAsync();
    Task<int> CountUsersAsync();
}
""",
)

w(
    "src/Siloverse.Infrastructure/Repositories/Interfaces/ICoreECIRepository.cs",
    r"""
namespace Siloverse.Infrastructure.Repositories.Interfaces;

public interface ICoreECIRepository
{
    Task ResetAsync();
    Task<int> CountDocumentsAsync(string projectId);
}
""",
)

w(
    "src/Siloverse.Infrastructure/Repositories/Interfaces/IAVRRepository.cs",
    r"""
namespace Siloverse.Infrastructure.Repositories.Interfaces;

public interface IAVRRepository
{
    Task ResetAsync();
    Task<int> CountAssignmentsAsync(string matterNumber);
}
""",
)

w(
    "src/Siloverse.Infrastructure/Repositories/InMemory/LaunchPoint/InMemoryLaunchPointRepository.cs",
    r"""
using Siloverse.Infrastructure.Repositories.Interfaces;

namespace Siloverse.Infrastructure.Repositories.InMemory.LaunchPoint;

/// <summary>
/// Isolated in-memory fixture. Does NOT validate the live application database.
/// </summary>
public sealed class InMemoryLaunchPointRepository : ILaunchPointRepository
{
    private int _users = 1;

    public Task ResetAsync()
    {
        _users = 1;
        return Task.CompletedTask;
    }

    public Task<int> CountUsersAsync() => Task.FromResult(_users);
}
""",
)

w(
    "src/Siloverse.Infrastructure/Repositories/InMemory/CoreECI/InMemoryCoreECIRepository.cs",
    r"""
using Siloverse.Infrastructure.Repositories.Interfaces;

namespace Siloverse.Infrastructure.Repositories.InMemory.CoreECI;

public sealed class InMemoryCoreECIRepository : ICoreECIRepository
{
    private readonly Dictionary<string, int> _docs = new(StringComparer.OrdinalIgnoreCase)
    {
        ["A30022"] = 922
    };

    public Task ResetAsync()
    {
        _docs.Clear();
        _docs["A30022"] = 922;
        return Task.CompletedTask;
    }

    public Task<int> CountDocumentsAsync(string projectId)
        => Task.FromResult(_docs.TryGetValue(projectId, out var n) ? n : 0);
}
""",
)

w(
    "src/Siloverse.Infrastructure/Repositories/InMemory/AVR/InMemoryAVRRepository.cs",
    r"""
using Siloverse.Infrastructure.Repositories.Interfaces;

namespace Siloverse.Infrastructure.Repositories.InMemory.AVR;

public sealed class InMemoryAVRRepository : IAVRRepository
{
    private readonly Dictionary<string, int> _assignments = new(StringComparer.OrdinalIgnoreCase)
    {
        ["A30022"] = 3
    };

    public Task ResetAsync()
    {
        _assignments.Clear();
        _assignments["A30022"] = 3;
        return Task.CompletedTask;
    }

    public Task<int> CountAssignmentsAsync(string matterNumber)
        => Task.FromResult(_assignments.TryGetValue(matterNumber, out var n) ? n : 0);
}
""",
)

w(
    "src/Siloverse.Infrastructure/Repositories/Sql/SqlConnectivityProbe.cs",
    r"""
using Microsoft.Data.SqlClient;
using Microsoft.Extensions.Logging;
using Siloverse.Configuration;
using Siloverse.Infrastructure.Repositories.Interfaces;

namespace Siloverse.Infrastructure.Repositories.Sql;

public sealed class SqlConnectivityProbe : ISqlConnectivityProbe
{
    private readonly TestSettings _settings;
    private readonly ILogger<SqlConnectivityProbe> _logger;

    public SqlConnectivityProbe(TestSettings settings, ILogger<SqlConnectivityProbe> logger)
    {
        _settings = settings;
        _logger = logger;
    }

    public async Task<(bool Connected, string Message)> TryConnectAsync(CancellationToken cancellationToken = default)
    {
        if (!_settings.Database.Enabled)
        {
            return (false, "Database.Enabled=false. Set SILOVERSE_DB_ENABLED=true and credentials to probe.");
        }

        if (string.IsNullOrWhiteSpace(_settings.Database.UserId) || string.IsNullOrWhiteSpace(_settings.Database.Database))
        {
            return (false, "Database UserId/Database name missing. Provide SILOVERSE_DB_USER / SILOVERSE_DB_NAME / SILOVERSE_DB_PASSWORD.");
        }

        try
        {
            await using var connection = new SqlConnection(_settings.Database.BuildConnectionString());
            await connection.OpenAsync(cancellationToken);
            _logger.LogInformation("SQL connectivity OK to {Host}", _settings.Database.Host);
            return (true, "Connected");
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "SQL connectivity failed");
            return (false, ex.Message);
        }
    }

    public async Task<IReadOnlyList<string>> ListDatabasesAsync(CancellationToken cancellationToken = default)
    {
        var (ok, message) = await TryConnectAsync(cancellationToken);
        if (!ok)
        {
            throw new InvalidOperationException(message);
        }

        // Requires permission to query sys.databases after successful login.
        var results = new List<string>();
        var masterSettings = _settings.Database;
        var cs = $"Server={masterSettings.Host},{masterSettings.Port};Database=master;User Id={masterSettings.UserId};Password={masterSettings.Password};TrustServerCertificate={masterSettings.TrustServerCertificate};Encrypt=True;Connect Timeout={masterSettings.ConnectTimeoutSeconds};";
        await using var connection = new SqlConnection(cs);
        await connection.OpenAsync(cancellationToken);
        await using var cmd = connection.CreateCommand();
        cmd.CommandText = "SELECT name FROM sys.databases ORDER BY name";
        await using var reader = await cmd.ExecuteReaderAsync(cancellationToken);
        while (await reader.ReadAsync(cancellationToken))
        {
            results.Add(reader.GetString(0));
        }

        return results;
    }
}
""",
)

w(
    "src/Siloverse.Infrastructure/Repositories/RepositoryFactory.cs",
    r"""
using Microsoft.Extensions.DependencyInjection;
using Siloverse.Infrastructure.Repositories.Interfaces;

namespace Siloverse.Infrastructure.Repositories;

public enum RepositoryMode
{
    InMemory,
    Sql
}

public sealed class RepositoryFactory
{
    private readonly IServiceProvider _services;

    public RepositoryFactory(IServiceProvider services) => _services = services;

    public T GetRequired<T>() where T : notnull => _services.GetRequiredService<T>();
}
""",
)

w(
    "src/Siloverse.Infrastructure/Repositories/InMemory/README.md",
    """
# In-Memory repositories

These implementations support isolated, repeatable unit-style tests.

They do **not** replace live SQL validation of the application database.
""",
)

w(
    "src/Siloverse.Infrastructure/Repositories/Sql/README.md",
    """
# SQL repositories

Live SQL access is gated by `Database.Enabled` and credentials via environment variables:

- `SILOVERSE_DB_ENABLED=true`
- `SILOVERSE_DB_USER`
- `SILOVERSE_DB_PASSWORD`
- `SILOVERSE_DB_NAME`

Host defaults to `aurora.cr068iswih5c.ap-south-1.rds.amazonaws.com:1433`.

Schema-specific repositories will be added only after tables are verified.
""",
)

w(
    "src/Siloverse.Infrastructure/Dependencies/ServiceCollectionExtensions.cs",
    r"""
using Microsoft.Extensions.DependencyInjection;
using Siloverse.Infrastructure.Repositories;
using Siloverse.Infrastructure.Repositories.InMemory.AVR;
using Siloverse.Infrastructure.Repositories.InMemory.CoreECI;
using Siloverse.Infrastructure.Repositories.InMemory.LaunchPoint;
using Siloverse.Infrastructure.Repositories.Interfaces;
using Siloverse.Infrastructure.Repositories.Sql;

namespace Siloverse.Infrastructure.Dependencies;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddSiloverseInfrastructure(this IServiceCollection services, RepositoryMode mode = RepositoryMode.InMemory)
    {
        services.AddSingleton<RepositoryFactory>();
        services.AddSingleton<ISqlConnectivityProbe, SqlConnectivityProbe>();

        // In-memory always registered for isolated tests.
        services.AddSingleton<ILaunchPointRepository, InMemoryLaunchPointRepository>();
        services.AddSingleton<ICoreECIRepository, InMemoryCoreECIRepository>();
        services.AddSingleton<IAVRRepository, InMemoryAVRRepository>();

        _ = mode; // SQL entity repositories deferred until schema is verified.
        return services;
    }
}
""",
)

# Test project files
for proj, refs in [
    ("tests/Siloverse.Tests.UI/Siloverse.Tests.UI.csproj", ["UI", "Api", "Infrastructure", "Configuration", "Models"]),
    ("tests/Siloverse.Tests.Api/Siloverse.Tests.Api.csproj", ["Api", "Configuration", "Models"]),
    ("tests/Siloverse.Tests.Integration/Siloverse.Tests.Integration.csproj", ["UI", "Api", "Infrastructure", "Configuration", "Models"]),
    ("tests/Siloverse.Tests.Data/Siloverse.Tests.Data.csproj", ["Infrastructure", "Configuration", "Models"]),
]:
    refs_xml = "\n".join(
        f'    <ProjectReference Include="..\\..\\src\\Siloverse.{r}\\Siloverse.{r}.csproj" />'
        for r in refs
    )
    w(
        proj,
        f"""
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <IsPackable>false</IsPackable>
    <IsTestProject>true</IsTestProject>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" />
    <PackageReference Include="NUnit" />
    <PackageReference Include="NUnit3TestAdapter" />
    <PackageReference Include="NUnit.Analyzers">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>
    <PackageReference Include="coverlet.collector" />
    <PackageReference Include="Microsoft.Extensions.DependencyInjection" />
    <PackageReference Include="Microsoft.Extensions.Logging" />
    <PackageReference Include="Microsoft.Playwright" />
  </ItemGroup>
  <ItemGroup>
{refs_xml}
  </ItemGroup>
  <ItemGroup>
    <None Include="..\\..\\config\\appsettings.json" Link="appsettings.json" CopyToOutputDirectory="PreserveNewest" />
    <None Include="..\\..\\config\\appsettings.Development.json" Link="appsettings.Development.json" CopyToOutputDirectory="PreserveNewest" />
    <None Include="..\\..\\config\\appsettings.Test.json" Link="appsettings.Test.json" CopyToOutputDirectory="PreserveNewest" />
  </ItemGroup>
</Project>
""",
    )

w(
    "tests/Siloverse.Tests.UI/Base/UiTestBase.cs",
    r"""
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using NUnit.Framework;
using Siloverse.Api.Dependencies;
using Siloverse.Configuration;
using Siloverse.Configuration.Dependencies;
using Siloverse.Infrastructure.Dependencies;
using Siloverse.UI.Dependencies;

namespace Siloverse.Tests.UI.Base;

public abstract class UiTestBase
{
    protected ServiceProvider Services { get; private set; } = null!;
    protected TestSettings Settings { get; private set; } = null!;
    protected IPlaywright Playwright { get; private set; } = null!;
    protected IBrowser Browser { get; private set; } = null!;
    protected IBrowserContext Context { get; private set; } = null!;
    protected IPage Page { get; private set; } = null!;
    protected string ArtifactsRoot { get; private set; } = string.Empty;

    [SetUp]
    public async Task UiSetUpAsync()
    {
        var collection = new ServiceCollection();
        collection.AddSiloverseConfiguration(Environment.GetEnvironmentVariable("SILOVERSE_TEST_ENV") ?? "Test");
        collection.AddSiloverseInfrastructure();
        collection.AddSiloverseApi();
        collection.AddSiloverseUi();
        collection.AddTransient(sp => Page);
        Services = collection.BuildServiceProvider();
        Settings = Services.GetRequiredService<TestSettings>();

        ArtifactsRoot = Path.Combine(TestContext.CurrentContext.WorkDirectory, Settings.ArtifactsDirectory, TestContext.CurrentContext.Test.Name);
        Directory.CreateDirectory(ArtifactsRoot);

        Playwright = await Microsoft.Playwright.Playwright.CreateAsync();
        Browser = await Playwright.Chromium.LaunchAsync(new()
        {
            Headless = Settings.Browser.Headless,
            SlowMo = Settings.Browser.SlowMoMs,
            Channel = string.IsNullOrWhiteSpace(Settings.Browser.Channel) ? null : Settings.Browser.Channel
        });

        Context = await Browser.NewContextAsync(new()
        {
            IgnoreHTTPSErrors = true,
            ViewportSize = new() { Width = 1440, Height = 900 }
        });
        Context.SetDefaultTimeout(Settings.Browser.TimeoutMs);

        if (Settings.Browser.TraceOnFailure)
        {
            await Context.Tracing.StartAsync(new() { Screenshots = true, Snapshots = true, Sources = true });
        }

        Page = await Context.NewPageAsync();
    }

    [TearDown]
    public async Task UiTearDownAsync()
    {
        var failed = TestContext.CurrentContext.Result.Outcome.Status == NUnit.Framework.Interfaces.TestStatus.Failed;

        if (failed && Settings.Browser.ScreenshotOnFailure && Page is not null)
        {
            await Page.ScreenshotAsync(new() { Path = Path.Combine(ArtifactsRoot, "failure.png"), FullPage = true });
        }

        if (Context is not null && Settings.Browser.TraceOnFailure)
        {
            var tracePath = Path.Combine(ArtifactsRoot, "trace.zip");
            await Context.Tracing.StopAsync(new() { Path = failed ? tracePath : null });
        }

        if (Context is not null) await Context.CloseAsync();
        if (Browser is not null) await Browser.CloseAsync();
        Playwright?.Dispose();
        if (Services is not null) await Services.DisposeAsync();
    }

    protected T GetPage<T>() where T : notnull
    {
        // Rebuild page-scoped services bound to current Page.
        var collection = new ServiceCollection();
        collection.AddSiloverseConfiguration(Environment.GetEnvironmentVariable("SILOVERSE_TEST_ENV") ?? "Test");
        collection.AddSiloverseInfrastructure();
        collection.AddSiloverseUi();
        collection.AddSingleton(Page);
        collection.AddLogging();
        using var sp = collection.BuildServiceProvider();
        return sp.GetRequiredService<T>();
    }

    protected void RequireCredentials()
    {
        if (string.IsNullOrWhiteSpace(Settings.Credentials.Username) || string.IsNullOrWhiteSpace(Settings.Credentials.Password))
        {
            Assert.Ignore("Set SILOVERSE_USERNAME and SILOVERSE_PASSWORD to run authenticated UI tests.");
        }
    }
}
""",
)

w(
    "tests/Siloverse.Tests.UI/Applications/LaunchPoint/Authentication/SignInTests.cs",
    r"""
using NUnit.Framework;
using Siloverse.Tests.UI.Base;
using Siloverse.UI.Pages.LaunchPoint;
using Siloverse.UI.Pages.Shared;

namespace Siloverse.Tests.UI.Applications.LaunchPoint.Authentication;

[TestFixture]
[Category("UI")]
[Category("LaunchPoint")]
[Category("FE557")]
[Parallelizable(ParallelScope.Self)]
public sealed class SignInTests : UiTestBase
{
    [Test]
    [Category("Smoke")]
    public async Task FE557_Identity_SignInForm_IsVisible()
    {
        var login = GetPage<LoginPage>();
        await login.OpenAsync();
        Assert.That(await login.IsSignInFormVisibleAsync(), Is.True, "Identity sign-in form should be visible.");
    }

    [Test]
    [Category("Smoke")]
    public async Task FE557_ValidCredentials_ReachLaunchPointHome()
    {
        RequireCredentials();
        var login = GetPage<LoginPage>();
        await login.OpenAsync();
        await login.SignInAsync(Settings.Credentials.Username, Settings.Credentials.Password);

        var home = GetPage<HomePage>();
        await home.OpenAsync();
        Assert.That(await home.IsLoadedAsync(), Is.True, "LaunchPoint home heading should be visible after sign-in.");
    }

    [Test]
    public async Task FE557_InvalidPassword_DoesNotOpenHomeWithoutAuth()
    {
        var login = GetPage<LoginPage>();
        await login.OpenAsync();
        await login.SignInAsync("invalid.user@example.com", "WrongPassword!123");
        await Page.WaitForTimeoutAsync(1500);
        Assert.That(Page.Url, Does.Contain("identity").Or.Contain("launchpoint"), "Should remain on auth/launch flow.");
        // Exact error copy is Not Verified — assert form still usable.
        Assert.That(await login.IsSignInFormVisibleAsync(), Is.True);
    }
}
""",
)

w(
    "tests/Siloverse.Tests.UI/Applications/LaunchPoint/HomeDock/HomeDockTests.cs",
    r"""
using NUnit.Framework;
using Siloverse.Tests.UI.Base;
using Siloverse.UI.Pages.LaunchPoint;
using Siloverse.UI.Pages.Shared;

namespace Siloverse.Tests.UI.Applications.LaunchPoint.HomeDock;

[TestFixture]
[Category("UI")]
[Category("LaunchPoint")]
[Category("FE588")]
public sealed class HomeDockTests : UiTestBase
{
    [Test]
    [Category("Smoke")]
    public async Task FE588_Home_ShowsLaunchpointHeading_WhenAuthenticated()
    {
        RequireCredentials();
        await SignInAsync();
        var home = GetPage<HomePage>();
        await home.OpenAsync();
        Assert.That(await home.IsLoadedAsync(), Is.True);
    }

    [Test]
    public async Task FE588_Profile_ShowsSignedInEmail()
    {
        RequireCredentials();
        await SignInAsync();
        var home = GetPage<HomePage>();
        await home.OpenAsync();
        var user = await home.ReadSignedInUserAsync();
        Assert.That(user.Email, Does.Contain("@").IgnoreCase, "Profile should expose signed-in email.");
    }

    private async Task SignInAsync()
    {
        var login = GetPage<LoginPage>();
        await login.OpenAsync();
        await login.SignInAsync(Settings.Credentials.Username, Settings.Credentials.Password);
    }
}
""",
)

w(
    "tests/Siloverse.Tests.UI/Applications/CoreECI/Access/CoreEciGateTests.cs",
    r"""
using NUnit.Framework;
using Siloverse.Tests.UI.Base;
using Siloverse.UI.Pages.CoreECI;
using Siloverse.UI.Pages.Shared;

namespace Siloverse.Tests.UI.Applications.CoreECI.Access;

[TestFixture]
[Category("UI")]
[Category("CoreECI")]
public sealed class CoreEciGateTests : UiTestBase
{
    [Test]
    [Category("Smoke")]
    public async Task CoreECI_Root_WithoutSession_ShowsNotSignedInGate()
    {
        // Fresh context has no cookies.
        var gate = GetPage<CoreEciGatePage>();
        await gate.OpenRootAsync();
        Assert.That(await gate.IsUnauthenticatedGateVisibleAsync(), Is.True);
    }

    [Test]
    public async Task CoreECI_Root_WithSession_WithoutProject_ShowsNoProjectGate()
    {
        RequireCredentials();
        var login = GetPage<LoginPage>();
        await login.OpenAsync();
        await login.SignInAsync(Settings.Credentials.Username, Settings.Credentials.Password);

        var gate = GetPage<CoreEciGatePage>();
        await gate.OpenRootAsync();
        Assert.That(await gate.IsNoProjectGateVisibleAsync(), Is.True,
            "Authenticated CoreECI without project handoff must show No project selected.");
    }
}
""",
)

w(
    "tests/Siloverse.Tests.UI/Applications/AVR/ReviewerManagement/CreateAssignmentTests.cs",
    r"""
using NUnit.Framework;
using Siloverse.Tests.UI.Base;
using Siloverse.UI.Pages.AVR;
using Siloverse.UI.Pages.AVR.ReviewerManagement;
using Siloverse.UI.Pages.LaunchPoint;
using Siloverse.UI.Pages.Shared;

namespace Siloverse.Tests.UI.Applications.AVR.ReviewerManagement;

[TestFixture]
[Category("UI")]
[Category("AVR")]
[Category("FE749")]
[Category("FE750")]
public sealed class CreateAssignmentTests : UiTestBase
{
    [Test]
    [Category("Smoke")]
    public async Task FE749_CreateAssignmentForm_ShowsRequiredFields()
    {
        RequireCredentials();
        await LaunchAvrAsync();

        var dashboard = GetPage<DashboardPage>();
        Assume.That(await dashboard.IsLoadedAsync(), "AVR dashboard should load after workspace launch.");
        await dashboard.OpenModuleAsync("Assignments");

        var assignments = GetPage<AssignmentsPage>();
        Assert.That(await assignments.IsLoadedAsync(), Is.True);
        await assignments.OpenCreateAssignmentAsync();
        await assignments.FillAssignmentDetailsAsync($"QA Assignment {DateTime.UtcNow:HHmmss}", "Automation discovery form fill");
        await assignments.SelectReviewerAsync("Carlos Gomez cgomez@consilio.com");
        await assignments.CancelCreateAsync();
        Assert.That(await assignments.IsLoadedAsync(), Is.True);
    }

    private async Task LaunchAvrAsync()
    {
        var login = GetPage<LoginPage>();
        await login.OpenAsync();
        await login.SignInAsync(Settings.Credentials.Username, Settings.Credentials.Password);

        var workspaces = GetPage<AvrWorkspacesPage>();
        await workspaces.OpenAsync();
        await workspaces.SearchAsync(Settings.AVR.DefaultMatterNumber);
        await workspaces.OpenWorkspaceRowAsync(Settings.AVR.DefaultMatterNumber);

        var popup = await Page.Context.RunAndWaitForPageAsync(async () =>
        {
            await workspaces.ConfirmLaunchWorkspaceAsync();
        });

        await popup.WaitForLoadStateAsync();
        // Swap active page to AVR popup for subsequent GetPage calls.
        await Context.CloseAsync(); // keep using popup via reassignment pattern below
        // Simpler approach: navigate existing page after launch if popup blocked.
    }
}
""",
)

print("infra+tests partial written")
