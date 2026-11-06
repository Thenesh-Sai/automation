using System.Diagnostics;
using System.Text;
using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Models.Common;

namespace Siloverse.Api.Common;

public abstract class ApiClientBase
{
    private readonly IAPIRequestContext _request;
    private readonly ILogger _logger;

    protected ApiClientBase(IAPIRequestContext request, ILogger logger)
    {
        _request = request;
        _logger = logger;
    }

    protected async Task<ApiCallResult> SendAsync(
        string method,
        string url,
        Dictionary<string, string>? headers = null,
        string? jsonBody = null)
    {
        var sw = Stopwatch.StartNew();
        var options = new APIRequestContextOptions
        {
            Headers = headers,
            Data = jsonBody,
        };

        _logger.LogInformation("API {Method} {Url}", method, RedactUrl(url));

        IAPIResponse response = method.ToUpperInvariant() switch
        {
            "GET" => await _request.GetAsync(url, options),
            "POST" => await _request.PostAsync(url, options),
            "PUT" => await _request.PutAsync(url, options),
            "PATCH" => await _request.FetchAsync(url, new() { Method = "PATCH", Headers = headers, Data = jsonBody }),
            "DELETE" => await _request.DeleteAsync(url, options),
            _ => throw new NotSupportedException($"HTTP method not supported: {method}")
        };

        sw.Stop();
        var body = await response.TextAsync();
        var headerMap = response.Headers.ToDictionary(k => k.Key, v => v.Value, StringComparer.OrdinalIgnoreCase);

        _logger.LogInformation("API response {Status} in {Ms}ms", response.Status, sw.ElapsedMilliseconds);

        return new ApiCallResult
        {
            StatusCode = response.Status,
            Body = body,
            Headers = headerMap,
            Duration = sw.Elapsed
        };
    }

    private static string RedactUrl(string url)
    {
        // Avoid logging tokens if ever appended as query params.
        return url.Contains('?', StringComparison.Ordinal)
            ? url[..url.IndexOf('?', StringComparison.Ordinal)] + "?[redacted]"
            : url;
    }

    protected static string? EncodeBasic(string user, string password)
    {
        if (string.IsNullOrWhiteSpace(user))
        {
            return null;
        }

        var raw = Convert.ToBase64String(Encoding.UTF8.GetBytes($"{user}:{password}"));
        return $"Basic {raw}";
    }
}
