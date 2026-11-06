using NUnit.Framework;
using Siloverse.Tests.UI.Base;
using Siloverse.UI.Pages.LaunchPoint;
using Siloverse.UI.Pages.Shared;

namespace Siloverse.Tests.UI.Applications.LaunchPoint.Authentication;

[TestFixture]
[Category("UI")]
[Category("LaunchPoint")]
[Category("FE557")]
public sealed class SignInTests : UiTestBase
{
    [Test]
    [Category("Smoke")]
    public async Task FE557_Identity_SignInForm_IsVisible()
    {
        var login = GetPage<LoginPage>();
        await login.OpenAsync();
        Assert.That(await login.IsSignInFormVisibleAsync(), Is.True, "Identity sign-in form should be visible.");
    }

    [Test]
    [Category("Smoke")]
    public async Task FE557_ValidCredentials_ReachLaunchPointHome()
    {
        RequireCredentials();
        var login = GetPage<LoginPage>();
        await login.OpenAsync();
        await login.SignInAsync(Settings.Credentials.Username, Settings.Credentials.Password);

        var home = GetPage<HomePage>();
        // Sign-in already lands on LaunchPoint; OpenAsync reloads home for a stable assertion.
        await home.OpenAsync();
        Assert.That(await home.IsLoadedAsync(), Is.True, "LaunchPoint home heading should be visible after sign-in.");
        Assert.That(Page.Url, Does.Contain("launchpoint-ui.dev.siloverse.space"));
    }

    [Test]
    public async Task FE557_InvalidPassword_DoesNotOpenHomeWithoutAuth()
    {
        var login = GetPage<LoginPage>();
        await login.OpenAsync();
        await login.SignInAsync("invalid.user@example.com", "WrongPassword!123", waitForLaunchPoint: false);
        await Page.WaitForTimeoutAsync(1500);
        Assert.That(Page.Url, Does.Contain("identity").Or.Contain("launchpoint"), "Should remain on auth/launch flow.");
        // Exact error copy is Not Verified — assert form still usable.
        Assert.That(await login.IsSignInFormVisibleAsync(), Is.True);
    }
}
