using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Api.Common;
using Siloverse.Configuration;
using Siloverse.Models.Common;

namespace Siloverse.Api.Applications.LaunchPoint;

/// <summary>
/// LaunchPoint API surface. No business endpoints are implemented until OpenAPI/network capture verifies them.
/// </summary>
public sealed class LaunchPointApiClient : ApiClientBase
{
    private readonly TestSettings _settings;

    public LaunchPointApiClient(IAPIRequestContext request, TestSettings settings, ILogger<LaunchPointApiClient> logger)
        : base(request, logger)
    {
        _settings = settings;
    }

    public DiscoveryStatus ContractStatus => DiscoveryStatus.NotVerified;

    public Task<ApiCallResult> GetUiRootAsync()
        => SendAsync("GET", _settings.LaunchPoint.BaseUrl.TrimEnd('/') + "/");
}
