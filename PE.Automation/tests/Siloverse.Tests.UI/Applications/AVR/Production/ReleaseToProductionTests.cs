using NUnit.Framework;
using Siloverse.Tests.UI.Base;
using Siloverse.UI.Pages.AVR;
using Siloverse.UI.Pages.AVR.Production;

namespace Siloverse.Tests.UI.Applications.AVR.Production;

[TestFixture]
[Category("UI")]
[Category("AVR")]
[Category("FE531")]
public sealed class ReleaseToProductionTests : UiTestBase
{
    [Test]
    [Category("Smoke")]
    public async Task FE531_ProductionModule_ShowsNewPackageControl()
    {
        await SignInViaIdentityAsync();
        await LaunchAvrWorkspaceAsync(Settings.AVR.DefaultMatterNumber);

        var dashboard = GetPage<DashboardPage>();
        await dashboard.OpenModuleAsync("Release to Production");

        var production = GetPage<ReleaseToProductionPage>();
        Assert.That(await production.IsLoadedAsync(), Is.True);
        Assert.That(await production.IsNewPackageVisibleAsync(), Is.True);
    }
}
