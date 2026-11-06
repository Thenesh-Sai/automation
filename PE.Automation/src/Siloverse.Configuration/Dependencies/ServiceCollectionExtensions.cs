using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;

namespace Siloverse.Configuration.Dependencies;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddSiloverseConfiguration(this IServiceCollection services, string? environmentName = null)
    {
        var settings = ConfigurationLoader.LoadSettings(environmentName);
        services.AddSingleton(settings);
        services.AddLogging(builder =>
        {
            builder.ClearProviders();
            builder.AddConsole();
            builder.SetMinimumLevel(LogLevel.Information);
        });
        return services;
    }
}
