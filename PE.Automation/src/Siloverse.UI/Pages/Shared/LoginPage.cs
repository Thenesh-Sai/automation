using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Configuration;
using Siloverse.UI.Common;

namespace Siloverse.UI.Pages.Shared;

/// <summary>Identity UI — FE557 Sign In (Verified).</summary>
public sealed class LoginPage : BasePage
{
    public LoginPage(IPage page, TestSettings settings, ILogger<LoginPage> logger)
        : base(page, settings, logger)
    {
    }

    // Prefer id/placeholder — GetByLabel("Username") also matches "Remember my username" checkbox.
    private ILocator Username => Page.Locator("#corporate-user-name");
    private ILocator Password => Page.Locator("input[type='password']");
    private ILocator ContinueButton => ByRole(AriaRole.Button, "Continue to LaunchPoint");

    public async Task OpenAsync()
    {
        await GotoAsync(new NavigationHelper(Settings).IdentityRoot);
        await EnsureCorporateSignInFormAsync();
    }

    public async Task SignInAsync(string username, string password, bool waitForLaunchPoint = true)
    {
        await EnsureCorporateSignInFormAsync();
        await Username.FillAsync(username);
        await Password.FillAsync(password);
        await ContinueButton.ClickAsync();

        if (!waitForLaunchPoint)
        {
            return;
        }

        await Page.WaitForURLAsync(
            url => url.Contains("launchpoint-ui.dev.siloverse.space", StringComparison.OrdinalIgnoreCase),
            new PageWaitForURLOptions { Timeout = Settings.Browser.TimeoutMs });
        await Page.WaitForLoadStateAsync(LoadState.DOMContentLoaded);
        // Session cookies settle after the first LaunchPoint paint; wait for home heading.
        await Page.GetByRole(AriaRole.Heading, new()
        {
            NameRegex = new("Aurora Launchpoint", System.Text.RegularExpressions.RegexOptions.IgnoreCase)
        }).WaitForAsync(new LocatorWaitForOptions
        {
            State = WaitForSelectorState.Visible,
            Timeout = Settings.Browser.TimeoutMs
        });
    }

    /// <summary>
    /// Identity intermittently bounces through Azure AD SAML; recover back to the Consilio form.
    /// </summary>
    private async Task EnsureCorporateSignInFormAsync()
    {
        var identityRoot = new NavigationHelper(Settings).IdentityRoot;
        for (var attempt = 0; attempt < 4; attempt++)
        {
            if (await Username.IsVisibleAsync())
            {
                return;
            }

            if (Page.Url.Contains("microsoftonline.com", StringComparison.OrdinalIgnoreCase) ||
                Page.Url.Contains("login.microsoft", StringComparison.OrdinalIgnoreCase))
            {
                await GotoAsync(identityRoot);
                continue;
            }

            await Page.WaitForTimeoutAsync(1000);
        }

        await WaitHelper.WaitForVisibleAsync(Username, Settings.Browser.TimeoutMs);
    }

    public async Task<bool> IsSignInFormVisibleAsync()
        => await Username.IsVisibleAsync() && await Password.IsVisibleAsync();
}
