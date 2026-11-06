using NUnit.Framework;
using Siloverse.Tests.Integration.Base;
using Siloverse.UI.Pages.AVR;

namespace Siloverse.Tests.Integration.Applications.LaunchPointAvr;

[TestFixture]
[Category("Integration")]
[Category("LaunchPoint")]
[Category("AVR")]
public sealed class LaunchPointToAvrJourneyTests : IntegrationTestBase
{
    [Test]
    [Category("Smoke")]
    public async Task Identity_To_LaunchPoint_To_AVR_Dashboard_Succeeds()
    {
        await SignInViaIdentityAsync();
        await LaunchAvrWorkspaceAsync(Settings.AVR.DefaultMatterNumber);

        var dashboard = GetPage<DashboardPage>();
        Assert.That(await dashboard.IsLoadedAsync(), Is.True);
        Assert.That(Page.Url, Does.Contain("avr.dev.siloverse.space"));
    }
}
