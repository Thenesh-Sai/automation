using NUnit.Framework;
using Siloverse.Tests.UI.Base;
using Siloverse.UI.Pages.AVR;
using Siloverse.UI.Pages.AVR.DocumentAllocation;

namespace Siloverse.Tests.UI.Applications.AVR.DocumentAllocation;

[TestFixture]
[Category("UI")]
[Category("AVR")]
[Category("FE437")]
[Category("FE443")]
public sealed class DocumentSearchTests : UiTestBase
{
    [Test]
    [Category("Smoke")]
    public async Task FE437_DocumentsSearch_ReturnsMatterDocuments()
    {
        await SignInViaIdentityAsync();
        await LaunchAvrWorkspaceAsync(Settings.AVR.DefaultMatterNumber);

        var dashboard = GetPage<DashboardPage>();
        await dashboard.OpenModuleAsync("Documents");

        var documents = GetPage<DocumentsPage>();
        Assert.That(await documents.IsLoadedAsync(), Is.True);
        await documents.RunSearchAsync();

        var heading = await documents.ReadDocumentsHeadingAsync();
        Assert.That(heading, Does.Contain("Documents"), "Documents heading should render after search.");
        Assert.That(heading, Does.Match("Documents \\(\\s*\\d+\\s*\\)").IgnoreCase,
            "Expected document count in heading after search (observed behaviour requires Search click).");
    }

    [Test]
    public async Task FE443_SelectThisPage_EnablesAllocateWhenRowsExist()
    {
        await SignInViaIdentityAsync();
        await LaunchAvrWorkspaceAsync(Settings.AVR.DefaultMatterNumber);

        var dashboard = GetPage<DashboardPage>();
        await dashboard.OpenModuleAsync("Documents");
        var documents = GetPage<DocumentsPage>();
        await documents.RunSearchAsync();

        var heading = await documents.ReadDocumentsHeadingAsync();
        if (!heading.Contains("( 0 )") && !heading.Contains("(0)"))
        {
            await documents.SelectThisPageAsync();
            Assert.That(await documents.IsAllocateEnabledAsync(), Is.True);
        }
        else
        {
            Assert.Ignore("No documents returned for current filters; allocate enablement cannot be asserted.");
        }
    }
}
