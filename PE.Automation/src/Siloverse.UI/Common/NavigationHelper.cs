using Siloverse.Configuration;

namespace Siloverse.UI.Common;

public sealed class NavigationHelper
{
    private readonly TestSettings _settings;

    public NavigationHelper(TestSettings settings) => _settings = settings;

    public string LaunchPointHome => Combine(_settings.LaunchPoint.BaseUrl, _settings.LaunchPoint.HomePath);
    public string LaunchPointAvrWorkspaces => Combine(_settings.LaunchPoint.BaseUrl, _settings.LaunchPoint.AvrWorkspacesPath);
    public string IdentityRoot => _settings.LaunchPoint.IdentityUrl.TrimEnd('/') + "/";
    public string CoreEciRoot => _settings.CoreECI.BaseUrl.TrimEnd('/') + "/";
    public string AvrRoot => _settings.AVR.BaseUrl.TrimEnd('/') + "/";

    private static string Combine(string baseUrl, string path)
    {
        baseUrl = baseUrl.TrimEnd('/');
        path = string.IsNullOrWhiteSpace(path) ? "/" : (path.StartsWith('/') ? path : "/" + path);
        return baseUrl + path;
    }
}
