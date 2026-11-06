using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Configuration;
using Siloverse.UI.Common;

namespace Siloverse.UI.Pages.LaunchPoint;

/// <summary>LaunchPoint AVR workspace directory (Verified).</summary>
public sealed class AvrWorkspacesPage : BasePage
{
    public AvrWorkspacesPage(IPage page, TestSettings settings, ILogger<AvrWorkspacesPage> logger)
        : base(page, settings, logger)
    {
    }

    private ILocator Search => ByPlaceholder("Search workspace, matter name or ID...");
    private ILocator LaunchWorkspace => ByRole(AriaRole.Button, "Launch Workspace");
    private ILocator ModalHeading => Page.GetByRole(AriaRole.Heading, new() { Name = "Launch Workspace" });

    public async Task OpenAsync()
        => await GotoAsync(new NavigationHelper(Settings).LaunchPointAvrWorkspaces);

    public async Task SearchAsync(string term)
    {
        await WaitHelper.WaitForVisibleAsync(Search);
        await Search.FillAsync(term);
        await Page.Keyboard.PressAsync("Enter");
        await Page.WaitForTimeoutAsync(500);
    }

    public async Task OpenWorkspaceRowAsync(string matterNumber)
    {
        var row = Page.Locator("tr", new() { HasText = matterNumber }).First;
        await WaitHelper.WaitForVisibleAsync(row);
        await row.ClickAsync();
        await WaitHelper.WaitForVisibleAsync(ModalHeading);
    }

    public async Task ConfirmLaunchWorkspaceAsync()
    {
        await WaitHelper.WaitForVisibleAsync(LaunchWorkspace);
        await LaunchWorkspace.ClickAsync();
    }
}
