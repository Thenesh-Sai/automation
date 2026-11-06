using NUnit.Framework;
using Siloverse.Api.Applications.CoreECI;
using Siloverse.Models.Common;
using Siloverse.Tests.Api.Base;

namespace Siloverse.Tests.Api.Applications.CoreECI;

[TestFixture]
[Category("API")]
[Category("CoreECI")]
public sealed class CoreEciContractGateTests : ApiTestBase
{
    [Test]
    public void CoreECI_ApiContract_IsBlocked_UntilBaseUrlConfigured()
    {
        var client = Get<CoreECIApiClient>();
        Assert.That(client.ContractStatus, Is.EqualTo(DiscoveryStatus.Blocked).Or.EqualTo(DiscoveryStatus.NotVerified));
    }

    [Test]
    public async Task CoreECI_UiRoot_Responds()
    {
        var client = Get<CoreECIApiClient>();
        var result = await client.GetUiRootAsync();
        Assert.That(result.StatusCode, Is.EqualTo(200).Or.EqualTo(302).Or.EqualTo(301));
    }
}
