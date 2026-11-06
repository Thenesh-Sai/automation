using Siloverse.Infrastructure.Repositories.Interfaces;

namespace Siloverse.Infrastructure.Repositories.InMemory.AVR;

public sealed class InMemoryAVRRepository : IAVRRepository
{
    private readonly Dictionary<string, int> _assignments = new(StringComparer.OrdinalIgnoreCase)
    {
        ["A30022"] = 3
    };

    public Task ResetAsync()
    {
        _assignments.Clear();
        _assignments["A30022"] = 3;
        return Task.CompletedTask;
    }

    public Task<int> CountAssignmentsAsync(string matterNumber)
        => Task.FromResult(_assignments.TryGetValue(matterNumber, out var n) ? n : 0);
}
