using NUnit.Framework;
using Siloverse.Tests.Integration.Base;
using Siloverse.UI.Pages.CoreECI;

namespace Siloverse.Tests.Integration.Applications.LaunchPointCoreEci;

[TestFixture]
[Category("Integration")]
[Category("LaunchPoint")]
[Category("CoreECI")]
public sealed class CoreEciGateIntegrationTests : IntegrationTestBase
{
    [Test]
    public async Task AuthenticatedLaunchPointSession_StillRequiresCoreEciProjectHandoff()
    {
        await SignInViaIdentityAsync();
        var gate = GetPage<CoreEciGatePage>();
        await gate.OpenRootAsync();
        Assert.That(await gate.IsNoProjectGateVisibleAsync(), Is.True);
    }
}
