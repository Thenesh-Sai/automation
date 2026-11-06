using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Api.Common;
using Siloverse.Configuration;
using Siloverse.Models.Common;

namespace Siloverse.Api.Applications.AVR;

/// <summary>
/// AVR API client. Endpoint methods are intentionally withheld until contracts are Verified.
/// </summary>
public sealed class AVRApiClient : ApiClientBase
{
    private readonly TestSettings _settings;

    public AVRApiClient(IAPIRequestContext request, TestSettings settings, ILogger<AVRApiClient> logger)
        : base(request, logger)
    {
        _settings = settings;
    }

    public DiscoveryStatus ContractStatus =>
        string.IsNullOrWhiteSpace(_settings.AVR.ApiBaseUrl)
            ? DiscoveryStatus.Blocked
            : DiscoveryStatus.NotVerified;

    public Task<ApiCallResult> GetUiRootAsync()
        => SendAsync("GET", _settings.AVR.BaseUrl.TrimEnd('/') + "/");
}
