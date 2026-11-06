using NUnit.Framework;
using Siloverse.Infrastructure.Repositories.Interfaces;
using Siloverse.Tests.Data.Base;

namespace Siloverse.Tests.Data.Applications.InMemory;

[TestFixture]
[Category("Data")]
[Category("InMemory")]
public sealed class InMemoryRepositoryTests : DataTestBase
{
    [Test]
    public async Task LaunchPoint_InMemory_Reset_IsDeterministic()
    {
        var repo = Get<ILaunchPointRepository>();
        await repo.ResetAsync();
        Assert.That(await repo.CountUsersAsync(), Is.EqualTo(1));
    }

    [Test]
    public async Task CoreECI_InMemory_A30022_HasSeedDocuments()
    {
        var repo = Get<ICoreECIRepository>();
        await repo.ResetAsync();
        Assert.That(await repo.CountDocumentsAsync("A30022"), Is.EqualTo(922));
    }

    [Test]
    public async Task AVR_InMemory_A30022_HasSeedAssignments()
    {
        var repo = Get<IAVRRepository>();
        await repo.ResetAsync();
        Assert.That(await repo.CountAssignmentsAsync("A30022"), Is.EqualTo(3));
    }
}
