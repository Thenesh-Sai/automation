using NUnit.Framework;
using Siloverse.Api.Applications.LaunchPoint;
using Siloverse.Models.Common;
using Siloverse.Tests.Api.Base;

namespace Siloverse.Tests.Api.Applications.LaunchPoint;

[TestFixture]
[Category("API")]
[Category("LaunchPoint")]
public sealed class LaunchPointUiAvailabilityTests : ApiTestBase
{
    [Test]
    public async Task LaunchPoint_UiRoot_Responds()
    {
        var client = Get<LaunchPointApiClient>();
        Assert.That(client.ContractStatus, Is.EqualTo(DiscoveryStatus.NotVerified));

        var result = await client.GetUiRootAsync();
        Assert.That(result.StatusCode, Is.EqualTo(200).Or.EqualTo(302).Or.EqualTo(301),
            "UI host should respond; business API contracts remain Not Verified.");
    }
}
