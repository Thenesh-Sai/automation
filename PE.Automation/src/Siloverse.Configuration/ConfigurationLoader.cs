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
