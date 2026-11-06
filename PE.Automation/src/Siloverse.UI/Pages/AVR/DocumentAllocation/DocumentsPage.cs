using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Configuration;
using Siloverse.UI.Common;

namespace Siloverse.UI.Pages.AVR.DocumentAllocation;

/// <summary>FE437 Search Documents / FE443 Select Documents (Verified).</summary>
public sealed class DocumentsPage : BasePage
{
    public DocumentsPage(IPage page, TestSettings settings, ILogger<DocumentsPage> logger)
        : base(page, settings, logger)
    {
    }

    private ILocator Heading => Page.GetByRole(AriaRole.Heading, new() { NameRegex = new("^Documents") });
    private ILocator SearchBox => ByLabel("Search documents");
    private ILocator SearchButton => ByRole(AriaRole.Button, "Search");
    private ILocator AllocateSelected => Page.GetByRole(AriaRole.Button, new() { NameRegex = new("Allocate Selected") });

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

    public async Task RunSearchAsync(string? keyword = null)
    {
        if (!string.IsNullOrWhiteSpace(keyword))
        {
            await SearchBox.FillAsync(keyword);
        }

        await SearchButton.ClickAsync();
    }

    public async Task<string> ReadDocumentsHeadingAsync()
    {
        var h2 = Page.GetByRole(AriaRole.Heading, new() { Level = 2, NameRegex = new("Documents") });
        return (await h2.TextContentAsync())?.Trim() ?? string.Empty;
    }

    public async Task SelectThisPageAsync()
        => await Page.GetByRole(AriaRole.Button, new() { NameRegex = new("Select this page") }).ClickAsync();

    public async Task<bool> IsAllocateEnabledAsync()
        => await AllocateSelected.IsEnabledAsync();
}
