using Microsoft.Playwright;

namespace Siloverse.UI.Common;

public static class WaitHelper
{
    public static async Task WaitForVisibleAsync(ILocator locator, int timeoutMs = 30000)
        => await locator.WaitForAsync(new() { State = WaitForSelectorState.Visible, Timeout = timeoutMs });

    public static async Task WaitForHiddenAsync(ILocator locator, int timeoutMs = 30000)
        => await locator.WaitForAsync(new() { State = WaitForSelectorState.Hidden, Timeout = timeoutMs });
}
