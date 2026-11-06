using Microsoft.Extensions.DependencyInjection;
using Siloverse.Infrastructure.Repositories;
using Siloverse.Infrastructure.Repositories.InMemory.AVR;
using Siloverse.Infrastructure.Repositories.InMemory.CoreECI;
using Siloverse.Infrastructure.Repositories.InMemory.LaunchPoint;
using Siloverse.Infrastructure.Repositories.Interfaces;
using Siloverse.Infrastructure.Repositories.Sql;

namespace Siloverse.Infrastructure.Dependencies;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddSiloverseInfrastructure(this IServiceCollection services, RepositoryMode mode = RepositoryMode.InMemory)
    {
        services.AddSingleton<RepositoryFactory>();
        services.AddSingleton<ISqlConnectivityProbe, SqlConnectivityProbe>();

        // In-memory always registered for isolated tests.
        services.AddSingleton<ILaunchPointRepository, InMemoryLaunchPointRepository>();
        services.AddSingleton<ICoreECIRepository, InMemoryCoreECIRepository>();
        services.AddSingleton<IAVRRepository, InMemoryAVRRepository>();

        _ = mode; // SQL entity repositories deferred until schema is verified.
        return services;
    }
}
