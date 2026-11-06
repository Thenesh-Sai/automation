using NUnit.Framework;
using Siloverse.Tests.UI.Base;
using Siloverse.UI.Pages.LaunchPoint;

namespace Siloverse.Tests.UI.Applications.LaunchPoint.Authentication;

[TestFixture]
[Category("UI")]
[Category("LaunchPoint")]
public sealed class SignOutTests : UiTestBase
{
    [Test]
    public async Task SignOut_Control_IsAvailable_FromUserProfile()
    {
        await SignInViaIdentityAsync();
        var home = GetPage<HomePage>();
        await home.OpenAsync();
        await home.OpenUserProfileMenuAsync();
        Assert.That(await Page.GetByRole(Microsoft.Playwright.AriaRole.Button, new() { Name = "Sign Out" }).IsVisibleAsync(), Is.True);
    }
}
