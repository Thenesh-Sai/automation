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
