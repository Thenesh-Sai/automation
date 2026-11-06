using NUnit.Framework;
using Siloverse.Tests.UI.Base;
using Siloverse.UI.Pages.CoreECI;
using Siloverse.UI.Pages.Shared;

namespace Siloverse.Tests.UI.Applications.CoreECI.Access;

[TestFixture]
[Category("UI")]
[Category("CoreECI")]
public sealed class CoreEciGateTests : UiTestBase
{
    [Test]
    [Category("Smoke")]
    public async Task CoreECI_Root_WithoutSession_ShowsNotSignedInGate()
    {
        // Fresh context has no cookies.
        var gate = GetPage<CoreEciGatePage>();
        await gate.OpenRootAsync();
        Assert.That(await gate.IsUnauthenticatedGateVisibleAsync(), Is.True);
    }

    [Test]
    public async Task CoreECI_Root_WithSession_WithoutProject_ShowsNoProjectGate()
    {
        RequireCredentials();
        var login = GetPage<LoginPage>();
        await login.OpenAsync();
        await login.SignInAsync(Settings.Credentials.Username, Settings.Credentials.Password);

        var gate = GetPage<CoreEciGatePage>();
        await gate.OpenRootAsync();
        Assert.That(await gate.IsNoProjectGateVisibleAsync(), Is.True,
            "Authenticated CoreECI without project handoff must show No project selected.");
    }
}
