using NUnit.Framework;
using Siloverse.Tests.UI.Base;
using Siloverse.UI.Pages.AVR;
using Siloverse.UI.Pages.AVR.ReviewDocuments;

namespace Siloverse.Tests.UI.Applications.AVR.ReviewDocuments;

[TestFixture]
[Category("UI")]
[Category("AVR")]
[Category("FE394")]
[Category("FE395")]
[Category("FE396")]
[Category("FE747")]
public sealed class ReviewCodingTests : UiTestBase
{
    [Test]
    [Category("Smoke")]
    public async Task ReviewCodingPanel_ExposesVerifiedCodingControls()
    {
        await SignInViaIdentityAsync();
        await LaunchAvrWorkspaceAsync(Settings.AVR.DefaultMatterNumber);

        var dashboard = GetPage<DashboardPage>();
        await dashboard.OpenModuleAsync("Reviews");

        var coding = GetPage<ReviewCodingPage>();
        Assert.That(await coding.IsCodingPanelVisibleAsync(), Is.True,
            "Pending review document should expose Review Coding Panel.");

        await coding.SetResponsivenessAsync("Responsive");
        await coding.SetConfidentialityAsync("Not Confidential");
        await coding.SetPrivilegeAsync("Not Privileged");
        // Save draft only — avoid completing shared review data unless explicitly desired.
        await coding.SaveDraftAsync();
    }
}
