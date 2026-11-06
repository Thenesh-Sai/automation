# -*- coding: utf-8 -*-
"""Phase 2 scaffold writer for PE.Automation."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent


def w(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print("wrote", rel)


# ---------------------------------------------------------------------------
# Config JSON
# ---------------------------------------------------------------------------
w(
    "config/appsettings.json",
    r"""
{
  "EnvironmentName": "Development",
  "Browser": {
    "Headless": true,
    "SlowMoMs": 0,
    "TimeoutMs": 45000,
    "TraceOnFailure": true,
    "ScreenshotOnFailure": true,
    "VideoOnFailure": false,
    "Channel": "chromium"
  },
  "Credentials": {
    "Username": "",
    "Password": ""
  },
  "LaunchPoint": {
    "BaseUrl": "https://launchpoint-ui.dev.siloverse.space",
    "IdentityUrl": "https://identity.dev.siloverse.space",
    "HomePath": "/home",
    "AvrWorkspacesPath": "/avr/workspaces"
  },
  "CoreECI": {
    "BaseUrl": "https://coreeci.dev.siloverse.space",
    "ApiBaseUrl": "",
    "DefaultProjectId": "A30022"
  },
  "AVR": {
    "BaseUrl": "https://avr.dev.siloverse.space",
    "ApiBaseUrl": "",
    "DefaultMatterNumber": "A30022",
    "DefaultWorkspaceId": "539"
  },
  "Database": {
    "Provider": "SqlServer",
    "Host": "aurora.cr068iswih5c.ap-south-1.rds.amazonaws.com",
    "Port": 1433,
    "Database": "",
    "UserId": "",
    "Password": "",
    "TrustServerCertificate": true,
    "ConnectTimeoutSeconds": 15,
    "Enabled": false
  },
  "ArtifactsDirectory": "artifacts"
}
""",
)

w(
    "config/appsettings.Development.json",
    r"""
{
  "Browser": {
    "Headless": false
  }
}
""",
)

w(
    "config/appsettings.Test.json",
    r"""
{
  "Browser": {
    "Headless": true
  }
}
""",
)

# ---------------------------------------------------------------------------
# Siloverse.Configuration
# ---------------------------------------------------------------------------
w(
    "src/Siloverse.Configuration/Siloverse.Configuration.csproj",
    r"""
<Project Sdk="Microsoft.NET.Sdk">
  <ItemGroup>
    <PackageReference Include="Microsoft.Extensions.Configuration" />
    <PackageReference Include="Microsoft.Extensions.Configuration.Binder" />
    <PackageReference Include="Microsoft.Extensions.Configuration.EnvironmentVariables" />
    <PackageReference Include="Microsoft.Extensions.Configuration.Json" />
    <PackageReference Include="Microsoft.Extensions.Configuration.UserSecrets" />
    <PackageReference Include="Microsoft.Extensions.DependencyInjection" />
    <PackageReference Include="Microsoft.Extensions.Logging" />
    <PackageReference Include="Microsoft.Extensions.Logging.Console" />
  </ItemGroup>
  <ItemGroup>
    <None Include="..\..\config\appsettings.json" Link="appsettings.json" CopyToOutputDirectory="PreserveNewest" />
    <None Include="..\..\config\appsettings.Development.json" Link="appsettings.Development.json" CopyToOutputDirectory="PreserveNewest" />
    <None Include="..\..\config\appsettings.Test.json" Link="appsettings.Test.json" CopyToOutputDirectory="PreserveNewest" />
  </ItemGroup>
</Project>
""",
)

w(
    "src/Siloverse.Configuration/TestSettings.cs",
    r"""
namespace Siloverse.Configuration;

public sealed class TestSettings
{
    public string EnvironmentName { get; set; } = "Development";
    public BrowserSettings Browser { get; set; } = new();
    public CredentialSettings Credentials { get; set; } = new();
    public LaunchPointSettings LaunchPoint { get; set; } = new();
    public CoreEciSettings CoreECI { get; set; } = new();
    public AvrSettings AVR { get; set; } = new();
    public DatabaseSettings Database { get; set; } = new();
    public string ArtifactsDirectory { get; set; } = "artifacts";
}

public sealed class BrowserSettings
{
    public bool Headless { get; set; } = true;
    public int SlowMoMs { get; set; }
    public int TimeoutMs { get; set; } = 45000;
    public bool TraceOnFailure { get; set; } = true;
    public bool ScreenshotOnFailure { get; set; } = true;
    public bool VideoOnFailure { get; set; }
    public string Channel { get; set; } = "chromium";
}

public sealed class CredentialSettings
{
    public string Username { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
}

public sealed class LaunchPointSettings
{
    public string BaseUrl { get; set; } = string.Empty;
    public string IdentityUrl { get; set; } = string.Empty;
    public string HomePath { get; set; } = "/home";
    public string AvrWorkspacesPath { get; set; } = "/avr/workspaces";
}

public sealed class CoreEciSettings
{
    public string BaseUrl { get; set; } = string.Empty;
    public string ApiBaseUrl { get; set; } = string.Empty;
    public string DefaultProjectId { get; set; } = "A30022";
}

public sealed class AvrSettings
{
    public string BaseUrl { get; set; } = string.Empty;
    public string ApiBaseUrl { get; set; } = string.Empty;
    public string DefaultMatterNumber { get; set; } = "A30022";
    public string DefaultWorkspaceId { get; set; } = "539";
}

public sealed class DatabaseSettings
{
    public string Provider { get; set; } = "SqlServer";
    public string Host { get; set; } = string.Empty;
    public int Port { get; set; } = 1433;
    public string Database { get; set; } = string.Empty;
    public string UserId { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
    public bool TrustServerCertificate { get; set; } = true;
    public int ConnectTimeoutSeconds { get; set; } = 15;
    public bool Enabled { get; set; }

    public string BuildConnectionString()
    {
        return $"Server={Host},{Port};Database={Database};User Id={UserId};Password={Password};TrustServerCertificate={TrustServerCertificate};Encrypt=True;Connect Timeout={ConnectTimeoutSeconds};";
    }
}
""",
)

w(
    "src/Siloverse.Configuration/ConfigurationLoader.cs",
    r"""
using Microsoft.Extensions.Configuration;

namespace Siloverse.Configuration;

public static class ConfigurationLoader
{
    public static IConfigurationRoot BuildConfiguration(string? environmentName = null)
    {
        var env = environmentName
            ?? Environment.GetEnvironmentVariable("SILOVERSE_TEST_ENV")
            ?? Environment.GetEnvironmentVariable("DOTNET_ENVIRONMENT")
            ?? "Development";

        var basePath = FindConfigDirectory();

        return new ConfigurationBuilder()
            .SetBasePath(basePath)
            .AddJsonFile("appsettings.json", optional: false, reloadOnChange: false)
            .AddJsonFile($"appsettings.{env}.json", optional: true, reloadOnChange: false)
            .AddEnvironmentVariables(prefix: "SILOVERSE_")
            .Build();
    }

    public static TestSettings LoadSettings(string? environmentName = null)
    {
        var config = BuildConfiguration(environmentName);
        var settings = new TestSettings();
        config.Bind(settings);

        // Prefer env overrides for secrets (never hardcode credentials in source).
        settings.Credentials.Username = FirstNonEmpty(
            Environment.GetEnvironmentVariable("SILOVERSE_USERNAME"),
            settings.Credentials.Username);
        settings.Credentials.Password = FirstNonEmpty(
            Environment.GetEnvironmentVariable("SILOVERSE_PASSWORD"),
            settings.Credentials.Password);
        settings.Database.UserId = FirstNonEmpty(
            Environment.GetEnvironmentVariable("SILOVERSE_DB_USER"),
            settings.Database.UserId);
        settings.Database.Password = FirstNonEmpty(
            Environment.GetEnvironmentVariable("SILOVERSE_DB_PASSWORD"),
            settings.Database.Password);
        settings.Database.Database = FirstNonEmpty(
            Environment.GetEnvironmentVariable("SILOVERSE_DB_NAME"),
            settings.Database.Database);

        if (!string.IsNullOrWhiteSpace(Environment.GetEnvironmentVariable("SILOVERSE_DB_ENABLED")))
        {
            settings.Database.Enabled = bool.Parse(Environment.GetEnvironmentVariable("SILOVERSE_DB_ENABLED")!);
        }

        return settings;
    }

    private static string FindConfigDirectory()
    {
        var dir = new DirectoryInfo(AppContext.BaseDirectory);
        while (dir is not null)
        {
            var candidate = Path.Combine(dir.FullName, "config");
            if (File.Exists(Path.Combine(candidate, "appsettings.json")))
            {
                return candidate;
            }

            // Also accept copied appsettings next to binaries.
            if (File.Exists(Path.Combine(dir.FullName, "appsettings.json")))
            {
                return dir.FullName;
            }

            dir = dir.Parent;
        }

        return AppContext.BaseDirectory;
    }

    private static string FirstNonEmpty(params string?[] values)
        => values.FirstOrDefault(v => !string.IsNullOrWhiteSpace(v)) ?? string.Empty;
}
""",
)

w(
    "src/Siloverse.Configuration/Dependencies/ServiceCollectionExtensions.cs",
    r"""
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;

namespace Siloverse.Configuration.Dependencies;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddSiloverseConfiguration(this IServiceCollection services, string? environmentName = null)
    {
        var settings = ConfigurationLoader.LoadSettings(environmentName);
        services.AddSingleton(settings);
        services.AddLogging(builder =>
        {
            builder.ClearProviders();
            builder.AddConsole();
            builder.SetMinimumLevel(LogLevel.Information);
        });
        return services;
    }
}
""",
)

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
w(
    "src/Siloverse.Models/Siloverse.Models.csproj",
    r"""
<Project Sdk="Microsoft.NET.Sdk" />
""",
)

w(
    "src/Siloverse.Models/Common/ApiCallResult.cs",
    r"""
namespace Siloverse.Models.Common;

public sealed class ApiCallResult
{
    public required int StatusCode { get; init; }
    public string? Body { get; init; }
    public IReadOnlyDictionary<string, string> Headers { get; init; } = new Dictionary<string, string>();
    public TimeSpan Duration { get; init; }
    public bool IsSuccessStatusCode => StatusCode is >= 200 and < 300;
}
""",
)

w(
    "src/Siloverse.Models/Common/DiscoveryStatus.cs",
    r"""
namespace Siloverse.Models.Common;

public enum DiscoveryStatus
{
    Verified,
    PartiallyVerified,
    NotVerified,
    NotAccessible,
    NotImplemented,
    Blocked
}
""",
)

w(
    "src/Siloverse.Models/Applications/LaunchPoint/Responses/SignedInUser.cs",
    r"""
namespace Siloverse.Models.Applications.LaunchPoint.Responses;

public sealed class SignedInUser
{
    public string DisplayName { get; init; } = string.Empty;
    public string Email { get; init; } = string.Empty;
}
""",
)

# ---------------------------------------------------------------------------
# API (verified-only foundation)
# ---------------------------------------------------------------------------
w(
    "src/Siloverse.Api/Siloverse.Api.csproj",
    r"""
<Project Sdk="Microsoft.NET.Sdk">
  <ItemGroup>
    <ProjectReference Include="..\Siloverse.Configuration\Siloverse.Configuration.csproj" />
    <ProjectReference Include="..\Siloverse.Models\Siloverse.Models.csproj" />
  </ItemGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.Extensions.DependencyInjection" />
    <PackageReference Include="Microsoft.Extensions.Logging" />
    <PackageReference Include="Microsoft.Playwright" />
  </ItemGroup>
</Project>
""",
)

w(
    "src/Siloverse.Api/Common/ApiClientBase.cs",
    r"""
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
""",
)

w(
    "src/Siloverse.Api/Applications/LaunchPoint/LaunchPointApiClient.cs",
    r"""
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
""",
)

w(
    "src/Siloverse.Api/Applications/CoreECI/CoreECIApiClient.cs",
    r"""
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
""",
)

w(
    "src/Siloverse.Api/Applications/AVR/AVRApiClient.cs",
    r"""
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
""",
)

w(
    "src/Siloverse.Api/Dependencies/ServiceCollectionExtensions.cs",
    r"""
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Playwright;
using Siloverse.Api.Applications.AVR;
using Siloverse.Api.Applications.CoreECI;
using Siloverse.Api.Applications.LaunchPoint;
using Siloverse.Configuration;

namespace Siloverse.Api.Dependencies;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddSiloverseApi(this IServiceCollection services)
    {
        services.AddSingleton<IPlaywright>(_ => Playwright.CreateAsync().GetAwaiter().GetResult());
        services.AddSingleton<IAPIRequestContext>(sp =>
        {
            var playwright = sp.GetRequiredService<IPlaywright>();
            return playwright.APIRequest.NewContextAsync(new()
            {
                IgnoreHTTPSErrors = true,
                Timeout = sp.GetRequiredService<TestSettings>().Browser.TimeoutMs
            }).GetAwaiter().GetResult();
        });

        services.AddTransient<LaunchPointApiClient>();
        services.AddTransient<CoreECIApiClient>();
        services.AddTransient<AVRApiClient>();
        return services;
    }
}
""",
)

print("phase2 partial config/api done")
