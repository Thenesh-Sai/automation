using Microsoft.Extensions.DependencyInjection;
using Siloverse.Infrastructure.Repositories.Interfaces;

namespace Siloverse.Infrastructure.Repositories;

public enum RepositoryMode
{
    InMemory,
    Sql
}

public sealed class RepositoryFactory
{
    private readonly IServiceProvider _services;

    public RepositoryFactory(IServiceProvider services) => _services = services;

    public T GetRequired<T>() where T : notnull => _services.GetRequiredService<T>();
}
