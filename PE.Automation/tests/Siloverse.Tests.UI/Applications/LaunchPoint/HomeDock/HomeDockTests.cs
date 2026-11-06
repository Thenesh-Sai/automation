using NUnit.Framework;
using Siloverse.Tests.UI.Base;
using Siloverse.UI.Pages.LaunchPoint;
using Siloverse.UI.Pages.Shared;

namespace Siloverse.Tests.UI.Applications.LaunchPoint.HomeDock;

[TestFixture]
[Category("UI")]
[Category("LaunchPoint")]
[Category("FE588")]
public sealed class HomeDockTests : UiTestBase
{
    [Test]
    [Category("Smoke")]
    public async Task FE588_Home_ShowsLaunchpointHeading_WhenAuthenticated()
    {
        RequireCredentials();
        await SignInAsync();
        var home = GetPage<HomePage>();
        await home.OpenAsync();
        Assert.That(await home.IsLoadedAsync(), Is.True);
    }

    [Test]
    public async Task FE588_Profile_ShowsSignedInEmail()
    {
        RequireCredentials();
        await SignInAsync();
        var home = GetPage<HomePage>();
        await home.OpenAsync();
        var user = await home.ReadSignedInUserAsync();
        Assert.That(user.Email, Does.Contain("@").IgnoreCase, "Profile should expose signed-in email.");
    }

    private async Task SignInAsync()
    {
        var login = GetPage<LoginPage>();
        await login.OpenAsync();
        await login.SignInAsync(Settings.Credentials.Username, Settings.Credentials.Password);
    }
}
