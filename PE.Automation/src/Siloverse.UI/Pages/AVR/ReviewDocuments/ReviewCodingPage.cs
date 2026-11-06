using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Configuration;
using Siloverse.UI.Common;

namespace Siloverse.UI.Pages.AVR.ReviewDocuments;

/// <summary>FE394/FE395/FE396/FE747 (Verified). FE397/FE399/FE748 not asserted.</summary>
public sealed class ReviewCodingPage : BasePage
{
    public ReviewCodingPage(IPage page, TestSettings settings, ILogger<ReviewCodingPage> logger)
        : base(page, settings, logger)
    {
    }

    private ILocator CodingPanel => Page.GetByRole(AriaRole.Heading, new() { Name = "Review Coding Panel" });
    private ILocator Responsive => ByRole(AriaRole.Radio, "Responsive");
    private ILocator NotResponsive => ByRole(AriaRole.Radio, "Not Responsive");
    private ILocator TechnicalIssue => ByRole(AriaRole.Radio, "Technical Issue");
    private ILocator Confidential => ByRole(AriaRole.Radio, "Confidential");
    private ILocator NotConfidential => ByRole(AriaRole.Radio, "Not Confidential");
    private ILocator Privileged => ByRole(AriaRole.Radio, "Privileged");
    private ILocator NotPrivileged => ByRole(AriaRole.Radio, "Not Privileged");
    private ILocator SaveDraft => ByRole(AriaRole.Button, "Save Draft");
    private ILocator CompleteReview => ByRole(AriaRole.Button, "Complete Review");

    public async Task<bool> IsCodingPanelVisibleAsync()
    {
        try
        {
            await CodingPanel.WaitForAsync(new LocatorWaitForOptions
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

    public async Task SetResponsivenessAsync(string value)
        => await Page.GetByRole(AriaRole.Radio, new() { Name = value }).CheckAsync();

    public async Task SetConfidentialityAsync(string value)
        => await Page.GetByRole(AriaRole.Radio, new() { Name = value }).CheckAsync();

    public async Task SetPrivilegeAsync(string value)
        => await Page.GetByRole(AriaRole.Radio, new() { Name = value }).CheckAsync();

    public async Task SaveDraftAsync()
        => await SaveDraft.ClickAsync();

    public async Task CompleteReviewAsync()
        => await CompleteReview.ClickAsync();
}
