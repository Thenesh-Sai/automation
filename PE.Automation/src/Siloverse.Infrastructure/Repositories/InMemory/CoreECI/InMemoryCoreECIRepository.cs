using Siloverse.Infrastructure.Repositories.Interfaces;

namespace Siloverse.Infrastructure.Repositories.InMemory.CoreECI;

public sealed class InMemoryCoreECIRepository : ICoreECIRepository
{
    private readonly Dictionary<string, int> _docs = new(StringComparer.OrdinalIgnoreCase)
    {
        ["A30022"] = 922
    };

    public Task ResetAsync()
    {
        _docs.Clear();
        _docs["A30022"] = 922;
        return Task.CompletedTask;
    }

    public Task<int> CountDocumentsAsync(string projectId)
        => Task.FromResult(_docs.TryGetValue(projectId, out var n) ? n : 0);
}
