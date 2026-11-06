namespace Siloverse.Infrastructure.Repositories.Interfaces;

public interface ICoreECIRepository
{
    Task ResetAsync();
    Task<int> CountDocumentsAsync(string projectId);
}
