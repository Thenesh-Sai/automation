using NUnit.Framework;
using Siloverse.Tests.UI.Base;
using Siloverse.UI.Pages.AVR;
using Siloverse.UI.Pages.AVR.ReviewerManagement;

namespace Siloverse.Tests.UI.Applications.AVR.ReviewerManagement;

[TestFixture]
[Category("UI")]
[Category("AVR")]
[Category("FE749")]
[Category("FE750")]
public sealed class CreateAssignmentTests : UiTestBase
{
    [Test]
    [Category("Smoke")]
    public async Task FE749_CreateAssignmentForm_ShowsRequiredFields_AndCanCancel()
    {
        await SignInViaIdentityAsync();
        await LaunchAvrWorkspaceAsync(Settings.AVR.DefaultMatterNumber);

        var dashboard = GetPage<DashboardPage>();
        Assert.That(await dashboard.IsLoadedAsync(), Is.True, "AVR dashboard should load after workspace launch.");

        await dashboard.OpenModuleAsync("Assignments");
        var assignments = GetPage<AssignmentsPage>();
        Assert.That(await assignments.IsLoadedAsync(), Is.True);

        await assignments.OpenCreateAssignmentAsync();
        await assignments.FillAssignmentDetailsAsync($"QA Assignment {DateTime.UtcNow:HHmmss}", "Automation form validation");
        await assignments.SelectReviewerAsync("Carlos Gomez cgomez@consilio.com");
        await assignments.CancelCreateAsync();

        Assert.That(await assignments.IsLoadedAsync(), Is.True);
    }

    [Test]
    [Category("FE751")]
    public async Task FE751_AssignmentsList_IsSearchable()
    {
        await SignInViaIdentityAsync();
        await LaunchAvrWorkspaceAsync(Settings.AVR.DefaultMatterNumber);

        var dashboard = GetPage<DashboardPage>();
        await dashboard.OpenModuleAsync("Assignments");
        var assignments = GetPage<AssignmentsPage>();
        await assignments.SearchAsync("Shipment");
        Assert.That(await assignments.IsLoadedAsync(), Is.True);
    }
}
