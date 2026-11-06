namespace Siloverse.Infrastructure.Repositories.Interfaces;

public interface ILaunchPointRepository
{
    Task ResetAsync();
    Task<int> CountUsersAsync();
}
