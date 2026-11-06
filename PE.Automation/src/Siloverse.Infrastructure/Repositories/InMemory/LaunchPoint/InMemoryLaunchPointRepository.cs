using Siloverse.Infrastructure.Repositories.Interfaces;

namespace Siloverse.Infrastructure.Repositories.InMemory.LaunchPoint;

/// <summary>
/// Isolated in-memory fixture. Does NOT validate the live application database.
/// </summary>
public sealed class InMemoryLaunchPointRepository : ILaunchPointRepository
{
    private int _users = 1;

    public Task ResetAsync()
    {
        _users = 1;
        return Task.CompletedTask;
    }

    public Task<int> CountUsersAsync() => Task.FromResult(_users);
}
