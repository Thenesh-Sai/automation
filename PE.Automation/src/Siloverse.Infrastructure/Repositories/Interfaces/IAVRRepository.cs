namespace Siloverse.Infrastructure.Repositories.Interfaces;

public interface IAVRRepository
{
    Task ResetAsync();
    Task<int> CountAssignmentsAsync(string matterNumber);
}
