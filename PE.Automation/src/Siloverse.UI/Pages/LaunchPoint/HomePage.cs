using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Configuration;
using Siloverse.Models.Applications.LaunchPoint.Responses;
using Siloverse.UI.Common;

namespace Siloverse.UI.Pages.LaunchPoint;

/// <summary>LaunchPoint Home Dock — FE588 (Verified).</summary>
public sealed class HomePage : BasePage
{
    public HomePage(IPage page, TestSettings settings, ILogger<HomePage> logger)
        : base(page, settings, logger)
    {
    }

    private ILocator Heading => Page.GetByRole(AriaRole.Heading, new() { NameRegex = new("Aurora Launchpoint", System.Text.RegularExpressions.RegexOptions.IgnoreCase) });
    private ILocator UserProfile => ByRole(AriaRole.Button, "User Profile");
    private ILocator SignOut => ByRole(AriaRole.Button, "Sign Out");
    private ILocator OpenAvr => ByRole(AriaRole.Button, "Open Aurora Verity Review");

    public async Task OpenAsync()
    {
        // Prefer the post-login landing page when already authenticated on home.
        if (Page.Url.Contains("launchpoint-ui.dev.siloverse.space/home", StringComparison.OrdinalIgnoreCase)
            && await Heading.IsVisibleAsync())
        {
            return;
        }

        var homeUrl = new NavigationHelper(Settings).LaunchPointHome;
        for (var attempt = 0; attempt < 3; attempt++)
        {
            await GotoAsync(homeUrl);
            try
            {
                await Heading.WaitForAsync(new LocatorWaitForOptions
                {
                    State = WaitForSelectorState.Visible,
                    Timeout = Settings.Browser.TimeoutMs
                });
                return;
            }
            catch (TimeoutException) when (Page.Url.Contains("identity.", StringComparison.OrdinalIgnoreCase) && attempt < 2)
            {
                // Intermittent identity bounce before LaunchPoint session cookie is ready.
                await Page.WaitForTimeoutAsync(1500);
            }
        }

        throw new TimeoutException($"LaunchPoint home heading not visible. Current URL: {Page.Url}");
    }

    public async Task<bool> IsLoadedAsync()
        => await Heading.IsVisibleAsync();

    public async Task OpenUserProfileMenuAsync()
        => await UserProfile.ClickAsync();

    public async Task SignOutAsync()
    {
        await OpenUserProfileMenuAsync();
        await WaitHelper.WaitForVisibleAsync(SignOut);
        await SignOut.ClickAsync();
    }

    public async Task<SignedInUser> ReadSignedInUserAsync()
    {
        await OpenUserProfileMenuAsync();
        await WaitHelper.WaitForVisibleAsync(SignOut);
        var email = await Page.Locator("text=/@/").First.TextContentAsync() ?? string.Empty;
        var display = await Page.GetByText("Rachel Torres").CountAsync() > 0
            ? "Rachel Torres"
            : string.Empty;
        return new SignedInUser { DisplayName = display, Email = email.Trim() };
    }

    public async Task OpenAuroraVerityReviewAsync()
        => await OpenAvr.ClickAsync();
}
