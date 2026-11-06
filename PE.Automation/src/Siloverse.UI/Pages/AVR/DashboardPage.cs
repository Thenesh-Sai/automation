using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Configuration;
using Siloverse.UI.Common;

namespace Siloverse.UI.Pages.AVR;

public sealed class DashboardPage : BasePage
{
    public DashboardPage(IPage page, TestSettings settings, ILogger<DashboardPage> logger)
        : base(page, settings, logger)
    {
    }

    private ILocator ModuleNav => ByRole(AriaRole.Button, "Open module navigation");
    private ILocator ReviewSummary => Page.GetByRole(AriaRole.Heading, new() { Name = "Review Summary" });

    public async Task<bool> IsLoadedAsync()
    {
        try
        {
            await ReviewSummary.WaitForAsync(new LocatorWaitForOptions
            {
                State = WaitForSelectorState.Visible,
                Timeout = Settings.Browser.TimeoutMs
            });
            return true;
        }
        catch (TimeoutException)
        {
            return false;
        }
    }

    public async Task OpenModuleAsync(string moduleName)
    {
        // Desktop icon rail uses title=; expanded/narrow drawer exposes accessible name text.
        var byTitle = Page.Locator($"nav[aria-label='Modules'] button[title='{moduleName}']");
        var byRole = Page.GetByRole(AriaRole.Navigation, new() { Name = "Modules" })
            .GetByRole(AriaRole.Button, new() { Name = moduleName, Exact = true });
        var target = byTitle.Or(byRole);

        if (await target.CountAsync() == 0 || !await target.First.IsVisibleAsync())
        {
            if (await ModuleNav.CountAsync() > 0 && await ModuleNav.First.IsVisibleAsync())
            {
                await ModuleNav.ClickAsync();
            }

            await WaitHelper.WaitForVisibleAsync(target.First, Settings.Browser.TimeoutMs);
        }

        await target.First.ClickAsync();
        await WaitForModuleReadyAsync(moduleName);
    }

    private async Task WaitForModuleReadyAsync(string moduleName)
    {
        ILocator ready = moduleName switch
        {
            "Dashboard" => ReviewSummary,
            "Documents" => Page.GetByRole(AriaRole.Heading, new() { NameRegex = new("^Documents") }),
            "Assignments" => Page.GetByRole(AriaRole.Heading, new() { NameRegex = new("^Assignments") }),
            "Reviews" => Page.GetByRole(AriaRole.Heading, new() { Name = "Review Coding Panel" }),
            "Release to Production" => Page.GetByRole(AriaRole.Heading, new() { NameRegex = new("Release to Production") }),
            _ => Page.GetByRole(AriaRole.Heading, new() { NameRegex = new(moduleName) })
        };

        await ready.First.WaitForAsync(new LocatorWaitForOptions
        {
            State = WaitForSelectorState.Visible,
            Timeout = Settings.Browser.TimeoutMs
        });
    }
}
