# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def w(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print("wrote", rel)


w(
    "src/Siloverse.UI/Siloverse.UI.csproj",
    r"""
<Project Sdk="Microsoft.NET.Sdk">
  <ItemGroup>
    <ProjectReference Include="..\Siloverse.Configuration\Siloverse.Configuration.csproj" />
    <ProjectReference Include="..\Siloverse.Models\Siloverse.Models.csproj" />
  </ItemGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.Extensions.DependencyInjection" />
    <PackageReference Include="Microsoft.Extensions.Logging" />
    <PackageReference Include="Microsoft.Playwright" />
  </ItemGroup>
</Project>
""",
)

w(
    "src/Siloverse.UI/Common/WaitHelper.cs",
    r"""
using Microsoft.Playwright;

namespace Siloverse.UI.Common;

public static class WaitHelper
{
    public static async Task WaitForVisibleAsync(ILocator locator, int timeoutMs = 30000)
        => await locator.WaitForAsync(new() { State = WaitForSelectorState.Visible, Timeout = timeoutMs });

    public static async Task WaitForHiddenAsync(ILocator locator, int timeoutMs = 30000)
        => await locator.WaitForAsync(new() { State = WaitForSelectorState.Hidden, Timeout = timeoutMs });
}
""",
)

w(
    "src/Siloverse.UI/Common/BasePage.cs",
    r"""
using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Configuration;

namespace Siloverse.UI.Common;

public abstract class BasePage
{
    protected BasePage(IPage page, TestSettings settings, ILogger logger)
    {
        Page = page;
        Settings = settings;
        Logger = logger;
    }

    protected IPage Page { get; }
    protected TestSettings Settings { get; }
    protected ILogger Logger { get; }

    public string Url => Page.Url;

    public async Task GotoAsync(string url)
    {
        Logger.LogInformation("Navigate to {Url}", url);
        await Page.GotoAsync(url, new() { WaitUntil = WaitUntilState.DOMContentLoaded, Timeout = Settings.Browser.TimeoutMs });
    }

    public async Task WaitForNetworkIdleAsync()
        => await Page.WaitForLoadStateAsync(LoadState.NetworkIdle);

    protected ILocator ByRole(AriaRole role, string name)
        => Page.GetByRole(role, new() { Name = name });

    protected ILocator ByLabel(string label)
        => Page.GetByLabel(label);

    protected ILocator ByPlaceholder(string text)
        => Page.GetByPlaceholder(text);

    protected ILocator ByText(string text)
        => Page.GetByText(text);
}
""",
)

w(
    "src/Siloverse.UI/Common/NavigationHelper.cs",
    r"""
using Siloverse.Configuration;

namespace Siloverse.UI.Common;

public sealed class NavigationHelper
{
    private readonly TestSettings _settings;

    public NavigationHelper(TestSettings settings) => _settings = settings;

    public string LaunchPointHome => Combine(_settings.LaunchPoint.BaseUrl, _settings.LaunchPoint.HomePath);
    public string LaunchPointAvrWorkspaces => Combine(_settings.LaunchPoint.BaseUrl, _settings.LaunchPoint.AvrWorkspacesPath);
    public string IdentityRoot => _settings.LaunchPoint.IdentityUrl.TrimEnd('/') + "/";
    public string CoreEciRoot => _settings.CoreECI.BaseUrl.TrimEnd('/') + "/";
    public string AvrRoot => _settings.AVR.BaseUrl.TrimEnd('/') + "/";

    private static string Combine(string baseUrl, string path)
    {
        baseUrl = baseUrl.TrimEnd('/');
        path = string.IsNullOrWhiteSpace(path) ? "/" : (path.StartsWith('/') ? path : "/" + path);
        return baseUrl + path;
    }
}
""",
)

w(
    "src/Siloverse.UI/Pages/Shared/LoginPage.cs",
    r"""
using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Configuration;
using Siloverse.UI.Common;

namespace Siloverse.UI.Pages.Shared;

/// <summary>Identity UI — FE557 Sign In (Verified).</summary>
public sealed class LoginPage : BasePage
{
    public LoginPage(IPage page, TestSettings settings, ILogger<LoginPage> logger)
        : base(page, settings, logger)
    {
    }

    private ILocator Username => ByLabel("Username");
    private ILocator Password => ByLabel("Password");
    private ILocator ContinueButton => ByRole(AriaRole.Button, "Continue to LaunchPoint");

    public async Task OpenAsync()
        => await GotoAsync(new NavigationHelper(Settings).IdentityRoot);

    public async Task SignInAsync(string username, string password)
    {
        await WaitHelper.WaitForVisibleAsync(Username);
        await Username.FillAsync(username);
        await Password.FillAsync(password);
        await ContinueButton.ClickAsync();
    }

    public async Task<bool> IsSignInFormVisibleAsync()
        => await Username.IsVisibleAsync() && await Password.IsVisibleAsync();
}
""",
)

w(
    "src/Siloverse.UI/Pages/LaunchPoint/HomePage.cs",
    r"""
using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Configuration;
using Siloverse.Models.Applications.LaunchPoint.Responses;
using Siloverse.UI.Common;

namespace Siloverse.UI.Pages.LaunchPoint;

/// <summary>LaunchPoint Home Dock — FE588 (Verified).</summary>
public sealed class HomePage : BasePage
{
    public HomePage(IPage page, TestSettings settings, ILogger<HomePage> logger)
        : base(page, settings, logger)
    {
    }

    private ILocator Heading => Page.GetByRole(AriaRole.Heading, new() { Name = "Aurora Launchpoint" });
    private ILocator UserProfile => ByRole(AriaRole.Button, "User Profile");
    private ILocator SignOut => ByRole(AriaRole.Button, "Sign Out");
    private ILocator OpenAvr => ByRole(AriaRole.Button, "Open Aurora Verity Review");

    public async Task OpenAsync()
        => await GotoAsync(new NavigationHelper(Settings).LaunchPointHome);

    public async Task<bool> IsLoadedAsync()
        => await Heading.IsVisibleAsync();

    public async Task OpenUserProfileMenuAsync()
        => await UserProfile.ClickAsync();

    public async Task SignOutAsync()
    {
        await OpenUserProfileMenuAsync();
        await WaitHelper.WaitForVisibleAsync(SignOut);
        await SignOut.ClickAsync();
    }

    public async Task<SignedInUser> ReadSignedInUserAsync()
    {
        await OpenUserProfileMenuAsync();
        var name = (await Page.GetByText("@consilio.com").Locator("xpath=preceding-sibling::*[1]").TextContentAsync())
            ?? string.Empty;
        // Fallback: read visible email text.
        var emailLocator = Page.GetByText("@consilio.com");
        var email = await emailLocator.First.TextContentAsync() ?? string.Empty;
        var display = await Page.Locator("text=Rachel Torres").CountAsync() > 0 ? "Rachel Torres" : name.Trim();
        return new SignedInUser { DisplayName = display, Email = email.Trim() };
    }

    public async Task OpenAuroraVerityReviewAsync()
        => await OpenAvr.ClickAsync();
}
""",
)

w(
    "src/Siloverse.UI/Pages/LaunchPoint/AvrWorkspacesPage.cs",
    r"""
using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Configuration;
using Siloverse.UI.Common;

namespace Siloverse.UI.Pages.LaunchPoint;

/// <summary>LaunchPoint AVR workspace directory (Verified).</summary>
public sealed class AvrWorkspacesPage : BasePage
{
    public AvrWorkspacesPage(IPage page, TestSettings settings, ILogger<AvrWorkspacesPage> logger)
        : base(page, settings, logger)
    {
    }

    private ILocator Search => ByPlaceholder("Search workspace, matter name or ID...");
    private ILocator LaunchWorkspace => ByRole(AriaRole.Button, "Launch Workspace");

    public async Task OpenAsync()
        => await GotoAsync(new NavigationHelper(Settings).LaunchPointAvrWorkspaces);

    public async Task SearchAsync(string term)
    {
        await WaitHelper.WaitForVisibleAsync(Search);
        await Search.FillAsync(term);
    }

    public async Task OpenWorkspaceRowAsync(string matterNumber)
    {
        var row = Page.Locator("tr", new() { HasText = matterNumber }).First;
        await WaitHelper.WaitForVisibleAsync(row);
        await row.ClickAsync();
    }

    public async Task ConfirmLaunchWorkspaceAsync()
    {
        await WaitHelper.WaitForVisibleAsync(LaunchWorkspace);
        await LaunchWorkspace.ClickAsync();
    }
}
""",
)

w(
    "src/Siloverse.UI/Pages/CoreECI/CoreEciGatePage.cs",
    r"""
using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Configuration;
using Siloverse.UI.Common;

namespace Siloverse.UI.Pages.CoreECI;

/// <summary>
/// CoreECI access gates verified without inventing unopened modules.
/// Full FE137+ UI requires verified project handoff (currently Partially Verified / Blocked).
/// </summary>
public sealed class CoreEciGatePage : BasePage
{
    public CoreEciGatePage(IPage page, TestSettings settings, ILogger<CoreEciGatePage> logger)
        : base(page, settings, logger)
    {
    }

    private ILocator NotSignedIn => Page.GetByRole(AriaRole.Heading, new() { Name = "You are not signed in" });
    private ILocator NoProject => Page.GetByRole(AriaRole.Heading, new() { Name = "No project selected" });
    private ILocator GoToLaunchPoint => ByRole(AriaRole.Button, "Go to LaunchPoint to sign in");
    private ILocator BackToLaunchPoint => ByRole(AriaRole.Button, "Back to LaunchPoint");

    public async Task OpenRootAsync()
        => await GotoAsync(new NavigationHelper(Settings).CoreEciRoot);

    public async Task<bool> IsUnauthenticatedGateVisibleAsync()
        => await NotSignedIn.IsVisibleAsync();

    public async Task<bool> IsNoProjectGateVisibleAsync()
        => await NoProject.IsVisibleAsync();

    public async Task ClickGoToLaunchPointAsync()
        => await GoToLaunchPoint.ClickAsync();

    public async Task ClickBackToLaunchPointAsync()
        => await BackToLaunchPoint.ClickAsync();
}
""",
)

w(
    "src/Siloverse.UI/Pages/AVR/DashboardPage.cs",
    r"""
using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Configuration;
using Siloverse.UI.Common;

namespace Siloverse.UI.Pages.AVR;

public sealed class DashboardPage : BasePage
{
    public DashboardPage(IPage page, TestSettings settings, ILogger<DashboardPage> logger)
        : base(page, settings, logger)
    {
    }

    private ILocator ModuleNav => ByRole(AriaRole.Button, "Open module navigation");
    private ILocator ReviewSummary => Page.GetByRole(AriaRole.Heading, new() { Name = "Review Summary" });

    public async Task<bool> IsLoadedAsync()
        => await ReviewSummary.IsVisibleAsync();

    public async Task OpenModuleAsync(string moduleName)
    {
        await ModuleNav.ClickAsync();
        await ByRole(AriaRole.Button, moduleName).ClickAsync();
    }
}
""",
)

w(
    "src/Siloverse.UI/Pages/AVR/ReviewerManagement/AssignmentsPage.cs",
    r"""
using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Configuration;
using Siloverse.UI.Common;

namespace Siloverse.UI.Pages.AVR.ReviewerManagement;

/// <summary>FE749 Create Assignment / FE750 Add Reviewers / FE751 list (Verified / Partial).</summary>
public sealed class AssignmentsPage : BasePage
{
    public AssignmentsPage(IPage page, TestSettings settings, ILogger<AssignmentsPage> logger)
        : base(page, settings, logger)
    {
    }

    private ILocator Heading => Page.GetByRole(AriaRole.Heading, new() { Name = "Assignments" });
    private ILocator CreateAssignment => ByRole(AriaRole.Button, "Create Assignment");
    private ILocator Search => ByPlaceholder("Search by assignment name, ID, or description...");
    private ILocator AssignmentName => ByLabel("Assignment name *");
    private ILocator Description => ByLabel("Description");
    private ILocator Cancel => ByRole(AriaRole.Button, "Cancel");

    public async Task<bool> IsLoadedAsync()
        => await Heading.IsVisibleAsync();

    public async Task OpenCreateAssignmentAsync()
        => await CreateAssignment.ClickAsync();

    public async Task FillAssignmentDetailsAsync(string name, string description)
    {
        await WaitHelper.WaitForVisibleAsync(AssignmentName);
        await AssignmentName.FillAsync(name);
        await Description.FillAsync(description);
    }

    public async Task SelectReviewerAsync(string reviewerVisibleName)
    {
        var checkbox = Page.GetByRole(AriaRole.Checkbox, new() { Name = reviewerVisibleName });
        await checkbox.CheckAsync();
    }

    public async Task CancelCreateAsync()
        => await Cancel.ClickAsync();

    public async Task SearchAsync(string term)
    {
        await Search.FillAsync(term);
    }
}
""",
)

w(
    "src/Siloverse.UI/Pages/AVR/DocumentAllocation/DocumentsPage.cs",
    r"""
using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Configuration;
using Siloverse.UI.Common;

namespace Siloverse.UI.Pages.AVR.DocumentAllocation;

/// <summary>FE437 Search Documents / FE443 Select Documents (Verified).</summary>
public sealed class DocumentsPage : BasePage
{
    public DocumentsPage(IPage page, TestSettings settings, ILogger<DocumentsPage> logger)
        : base(page, settings, logger)
    {
    }

    private ILocator Heading => Page.GetByRole(AriaRole.Heading, new() { Name = "Documents", Exact = true });
    private ILocator SearchBox => ByLabel("Search documents");
    private ILocator SearchButton => ByRole(AriaRole.Button, "Search");
    private ILocator AllocateSelected => Page.GetByRole(AriaRole.Button, new() { NameRegex = new("Allocate Selected") });

    public async Task<bool> IsLoadedAsync()
        => await Heading.IsVisibleAsync();

    public async Task RunSearchAsync(string? keyword = null)
    {
        if (!string.IsNullOrWhiteSpace(keyword))
        {
            await SearchBox.FillAsync(keyword);
        }

        await SearchButton.ClickAsync();
    }

    public async Task<string> ReadDocumentsHeadingAsync()
    {
        var h2 = Page.GetByRole(AriaRole.Heading, new() { Level = 2, NameRegex = new("Documents") });
        return (await h2.TextContentAsync())?.Trim() ?? string.Empty;
    }

    public async Task SelectThisPageAsync()
        => await Page.GetByRole(AriaRole.Button, new() { NameRegex = new("Select this page") }).ClickAsync();

    public async Task<bool> IsAllocateEnabledAsync()
        => await AllocateSelected.IsEnabledAsync();
}
""",
)

w(
    "src/Siloverse.UI/Pages/AVR/ReviewDocuments/ReviewCodingPage.cs",
    r"""
using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Configuration;
using Siloverse.UI.Common;

namespace Siloverse.UI.Pages.AVR.ReviewDocuments;

/// <summary>FE394/FE395/FE396/FE747 (Verified). FE397/FE399/FE748 not asserted.</summary>
public sealed class ReviewCodingPage : BasePage
{
    public ReviewCodingPage(IPage page, TestSettings settings, ILogger<ReviewCodingPage> logger)
        : base(page, settings, logger)
    {
    }

    private ILocator CodingPanel => Page.GetByRole(AriaRole.Heading, new() { Name = "Review Coding Panel" });
    private ILocator Responsive => ByRole(AriaRole.Radio, "Responsive");
    private ILocator NotResponsive => ByRole(AriaRole.Radio, "Not Responsive");
    private ILocator TechnicalIssue => ByRole(AriaRole.Radio, "Technical Issue");
    private ILocator Confidential => ByRole(AriaRole.Radio, "Confidential");
    private ILocator NotConfidential => ByRole(AriaRole.Radio, "Not Confidential");
    private ILocator Privileged => ByRole(AriaRole.Radio, "Privileged");
    private ILocator NotPrivileged => ByRole(AriaRole.Radio, "Not Privileged");
    private ILocator SaveDraft => ByRole(AriaRole.Button, "Save Draft");
    private ILocator CompleteReview => ByRole(AriaRole.Button, "Complete Review");

    public async Task<bool> IsCodingPanelVisibleAsync()
        => await CodingPanel.IsVisibleAsync();

    public async Task SetResponsivenessAsync(string value)
        => await Page.GetByRole(AriaRole.Radio, new() { Name = value }).CheckAsync();

    public async Task SetConfidentialityAsync(string value)
        => await Page.GetByRole(AriaRole.Radio, new() { Name = value }).CheckAsync();

    public async Task SetPrivilegeAsync(string value)
        => await Page.GetByRole(AriaRole.Radio, new() { Name = value }).CheckAsync();

    public async Task SaveDraftAsync()
        => await SaveDraft.ClickAsync();

    public async Task CompleteReviewAsync()
        => await CompleteReview.ClickAsync();
}
""",
)

w(
    "src/Siloverse.UI/Pages/AVR/Production/ReleaseToProductionPage.cs",
    r"""
using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Configuration;
using Siloverse.UI.Common;

namespace Siloverse.UI.Pages.AVR.Production;

/// <summary>FE531 New production package (Verified). FE533/FE538 partial.</summary>
public sealed class ReleaseToProductionPage : BasePage
{
    public ReleaseToProductionPage(IPage page, TestSettings settings, ILogger<ReleaseToProductionPage> logger)
        : base(page, settings, logger)
    {
    }

    private ILocator Heading => Page.GetByRole(AriaRole.Heading, new() { Name = "Release to Production" });
    private ILocator NewPackage => ByRole(AriaRole.Button, "New production package");
    private ILocator SearchPackages => ByPlaceholder("Search packages…");

    public async Task<bool> IsLoadedAsync()
        => await Heading.IsVisibleAsync();

    public async Task<bool> IsNewPackageVisibleAsync()
        => await NewPackage.IsVisibleAsync();

    public async Task SearchPackagesAsync(string term)
        => await SearchPackages.FillAsync(term);
}
""",
)

w(
    "src/Siloverse.UI/Dependencies/ServiceCollectionExtensions.cs",
    r"""
using Microsoft.Extensions.DependencyInjection;
using Siloverse.UI.Pages.AVR;
using Siloverse.UI.Pages.AVR.DocumentAllocation;
using Siloverse.UI.Pages.AVR.Production;
using Siloverse.UI.Pages.AVR.ReviewDocuments;
using Siloverse.UI.Pages.AVR.ReviewerManagement;
using Siloverse.UI.Pages.CoreECI;
using Siloverse.UI.Pages.LaunchPoint;
using Siloverse.UI.Pages.Shared;
using Siloverse.UI.Common;

namespace Siloverse.UI.Dependencies;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddSiloverseUi(this IServiceCollection services)
    {
        services.AddSingleton<NavigationHelper>();
        services.AddTransient<LoginPage>();
        services.AddTransient<HomePage>();
        services.AddTransient<AvrWorkspacesPage>();
        services.AddTransient<CoreEciGatePage>();
        services.AddTransient<DashboardPage>();
        services.AddTransient<AssignmentsPage>();
        services.AddTransient<DocumentsPage>();
        services.AddTransient<ReviewCodingPage>();
        services.AddTransient<ReleaseToProductionPage>();
        return services;
    }
}
""",
)

# Remove default Class1.cs files later via script
print("UI scaffold written")
