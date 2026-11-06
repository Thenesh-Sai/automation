using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Configuration;
using Siloverse.UI.Common;

namespace Siloverse.UI.Pages.AVR.Production;

/// <summary>FE531 New production package (Verified). FE533/FE538 partial.</summary>
public sealed class ReleaseToProductionPage : BasePage
{
    public ReleaseToProductionPage(IPage page, TestSettings settings, ILogger<ReleaseToProductionPage> logger)
        : base(page, settings, logger)
    {
    }

    private ILocator Heading => Page.GetByRole(AriaRole.Heading, new() { NameRegex = new("Release to Production") });
    private ILocator NewPackage => ByRole(AriaRole.Button, "New production package");
    private ILocator SearchPackages => ByPlaceholder("Search packages…");

    public async Task<bool> IsLoadedAsync()
    {
        try
        {
            await Heading.First.WaitForAsync(new LocatorWaitForOptions
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

    public async Task<bool> IsNewPackageVisibleAsync()
        => await NewPackage.IsVisibleAsync();

    public async Task SearchPackagesAsync(string term)
        => await SearchPackages.FillAsync(term);
}
