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
