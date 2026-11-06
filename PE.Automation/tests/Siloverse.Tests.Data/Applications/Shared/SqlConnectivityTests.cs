using NUnit.Framework;
using Siloverse.Infrastructure.Repositories.Interfaces;
using Siloverse.Tests.Data.Base;

namespace Siloverse.Tests.Data.Applications.Shared;

[TestFixture]
[Category("Data")]
[Category("Database")]
public sealed class SqlConnectivityTests : DataTestBase
{
    [Test]
    public async Task SqlProbe_ReportsBlocked_WhenCredentialsMissing()
    {
        var probe = Get<ISqlConnectivityProbe>();
        var (connected, message) = await probe.TryConnectAsync();

        if (!Settings.Database.Enabled ||
            string.IsNullOrWhiteSpace(Settings.Database.UserId) ||
            string.IsNullOrWhiteSpace(Settings.Database.Database))
        {
            Assert.That(connected, Is.False);
            Assert.That(message, Does.Contain("Database").IgnoreCase.Or.Contain("missing").IgnoreCase.Or.Contain("Enabled"));
            Assert.Ignore($"SQL live tests blocked: {message}. Set SILOVERSE_DB_* env vars. SSMS registered servers had no saved RDS login.");
        }

        Assert.That(connected, Is.True, message);
    }
}
