using NUnit.Framework;
using Siloverse.Api.Applications.AVR;
using Siloverse.Models.Common;
using Siloverse.Tests.Api.Base;

namespace Siloverse.Tests.Api.Applications.AVR;

[TestFixture]
[Category("API")]
[Category("AVR")]
public sealed class AvrContractGateTests : ApiTestBase
{
    [Test]
    public void AVR_ApiContract_IsBlocked_UntilBaseUrlConfigured()
    {
        var client = Get<AVRApiClient>();
        Assert.That(client.ContractStatus, Is.EqualTo(DiscoveryStatus.Blocked).Or.EqualTo(DiscoveryStatus.NotVerified));
    }

    [Test]
    public async Task AVR_UiRoot_Responds()
    {
        var client = Get<AVRApiClient>();
        var result = await client.GetUiRootAsync();
        Assert.That(result.StatusCode, Is.EqualTo(200).Or.EqualTo(302).Or.EqualTo(301));
    }
}
