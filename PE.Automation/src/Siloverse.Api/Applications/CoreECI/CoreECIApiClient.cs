using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Api.Common;
using Siloverse.Configuration;
using Siloverse.Models.Common;

namespace Siloverse.Api.Applications.CoreECI;

/// <summary>
/// CoreECI API client. Endpoint methods are intentionally withheld until contracts are Verified.
/// </summary>
public sealed class CoreECIApiClient : ApiClientBase
{
    private readonly TestSettings _settings;

    public CoreECIApiClient(IAPIRequestContext request, TestSettings settings, ILogger<CoreECIApiClient> logger)
        : base(request, logger)
    {
        _settings = settings;
    }

    public DiscoveryStatus ContractStatus =>
        string.IsNullOrWhiteSpace(_settings.CoreECI.ApiBaseUrl)
            ? DiscoveryStatus.Blocked
            : DiscoveryStatus.NotVerified;

    public Task<ApiCallResult> GetUiRootAsync()
        => SendAsync("GET", _settings.CoreECI.BaseUrl.TrimEnd('/') + "/");
}
