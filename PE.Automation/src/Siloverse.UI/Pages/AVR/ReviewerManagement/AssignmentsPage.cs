using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Configuration;
using Siloverse.UI.Common;

namespace Siloverse.UI.Pages.AVR.ReviewerManagement;

/// <summary>FE749 Create Assignment / FE750 Add Reviewers / FE751 list (Verified / Partial).</summary>
public sealed class AssignmentsPage : BasePage
{
    public AssignmentsPage(IPage page, TestSettings settings, ILogger<AssignmentsPage> logger)
        : base(page, settings, logger)
    {
    }

    private ILocator Heading => Page.GetByRole(AriaRole.Heading, new() { Name = "Assignments" });
    private ILocator CreateAssignment => ByRole(AriaRole.Button, "Create Assignment");
    private ILocator Search => ByPlaceholder("Search by assignment name, ID, or description...");
    private ILocator AssignmentName => ByLabel("Assignment name *");
    private ILocator Description => ByLabel("Description");
    private ILocator Cancel => ByRole(AriaRole.Button, "Cancel");

    public async Task<bool> IsLoadedAsync()
    {
        try
        {
            await Heading.WaitForAsync(new LocatorWaitForOptions
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

    public async Task OpenCreateAssignmentAsync()
        => await CreateAssignment.ClickAsync();

    public async Task FillAssignmentDetailsAsync(string name, string description)
    {
        await WaitHelper.WaitForVisibleAsync(AssignmentName);
        await AssignmentName.FillAsync(name);
        await Description.FillAsync(description);
    }

    public async Task SelectReviewerAsync(string reviewerVisibleName)
    {
        var checkbox = Page.GetByRole(AriaRole.Checkbox, new() { Name = reviewerVisibleName });
        await checkbox.CheckAsync();
    }

    public async Task CancelCreateAsync()
        => await Cancel.ClickAsync();

    public async Task SearchAsync(string term)
    {
        await Search.FillAsync(term);
    }
}
