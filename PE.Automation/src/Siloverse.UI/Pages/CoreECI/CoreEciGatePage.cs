using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Configuration;
using Siloverse.UI.Common;

namespace Siloverse.UI.Pages.CoreECI;

/// <summary>
/// CoreECI access gates verified without inventing unopened modules.
/// Full FE137+ UI requires verified project handoff (currently Partially Verified / Blocked).
/// </summary>
public sealed class CoreEciGatePage : BasePage
{
    public CoreEciGatePage(IPage page, TestSettings settings, ILogger<CoreEciGatePage> logger)
        : base(page, settings, logger)
    {
    }

    private ILocator NotSignedIn => Page.GetByRole(AriaRole.Heading, new() { Name = "You are not signed in" });
    private ILocator NoProject => Page.GetByRole(AriaRole.Heading, new() { Name = "No project selected" });
    private ILocator GoToLaunchPoint => ByRole(AriaRole.Button, "Go to LaunchPoint to sign in");
    private ILocator BackToLaunchPoint => ByRole(AriaRole.Button, "Back to LaunchPoint");

    public async Task OpenRootAsync()
        => await GotoAsync(new NavigationHelper(Settings).CoreEciRoot);

    public async Task<bool> IsUnauthenticatedGateVisibleAsync()
    {
        try
        {
            await NotSignedIn.Or(GoToLaunchPoint).First.WaitForAsync(new LocatorWaitForOptions
            {
                State = WaitForSelectorState.Visible,
                Timeout = Settings.Browser.TimeoutMs
            });
            return await NotSignedIn.IsVisibleAsync() || await GoToLaunchPoint.IsVisibleAsync();
        }
        catch (TimeoutException)
        {
            return false;
        }
    }

    public async Task<bool> IsNoProjectGateVisibleAsync()
        => await NoProject.IsVisibleAsync();

    public async Task ClickGoToLaunchPointAsync()
        => await GoToLaunchPoint.ClickAsync();

    public async Task ClickBackToLaunchPointAsync()
        => await BackToLaunchPoint.ClickAsync();
}
