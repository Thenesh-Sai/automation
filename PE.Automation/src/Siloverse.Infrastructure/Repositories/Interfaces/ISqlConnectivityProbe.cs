namespace Siloverse.Infrastructure.Repositories.Interfaces;

public interface ISqlConnectivityProbe
{
    Task<(bool Connected, string Message)> TryConnectAsync(CancellationToken cancellationToken = default);
    Task<IReadOnlyList<string>> ListDatabasesAsync(CancellationToken cancellationToken = default);
}
