using Microsoft.Data.SqlClient;
using Microsoft.Extensions.Logging;
using Siloverse.Configuration;
using Siloverse.Infrastructure.Repositories.Interfaces;

namespace Siloverse.Infrastructure.Repositories.Sql;

public sealed class SqlConnectivityProbe : ISqlConnectivityProbe
{
    private readonly TestSettings _settings;
    private readonly ILogger<SqlConnectivityProbe> _logger;

    public SqlConnectivityProbe(TestSettings settings, ILogger<SqlConnectivityProbe> logger)
    {
        _settings = settings;
        _logger = logger;
    }

    public async Task<(bool Connected, string Message)> TryConnectAsync(CancellationToken cancellationToken = default)
    {
        if (!_settings.Database.Enabled)
        {
            return (false, "Database.Enabled=false. Set SILOVERSE_DB_ENABLED=true and credentials to probe.");
        }

        if (string.IsNullOrWhiteSpace(_settings.Database.UserId) || string.IsNullOrWhiteSpace(_settings.Database.Database))
        {
            return (false, "Database UserId/Database name missing. Provide SILOVERSE_DB_USER / SILOVERSE_DB_NAME / SILOVERSE_DB_PASSWORD.");
        }

        try
        {
            await using var connection = new SqlConnection(_settings.Database.BuildConnectionString());
            await connection.OpenAsync(cancellationToken);
            _logger.LogInformation("SQL connectivity OK to {Host}", _settings.Database.Host);
            return (true, "Connected");
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "SQL connectivity failed");
            return (false, ex.Message);
        }
    }

    public async Task<IReadOnlyList<string>> ListDatabasesAsync(CancellationToken cancellationToken = default)
    {
        var (ok, message) = await TryConnectAsync(cancellationToken);
        if (!ok)
        {
            throw new InvalidOperationException(message);
        }

        // Requires permission to query sys.databases after successful login.
        var results = new List<string>();
        var masterSettings = _settings.Database;
        var cs = $"Server={masterSettings.Host},{masterSettings.Port};Database=master;User Id={masterSettings.UserId};Password={masterSettings.Password};TrustServerCertificate={masterSettings.TrustServerCertificate};Encrypt=True;Connect Timeout={masterSettings.ConnectTimeoutSeconds};";
        await using var connection = new SqlConnection(cs);
        await connection.OpenAsync(cancellationToken);
        await using var cmd = connection.CreateCommand();
        cmd.CommandText = "SELECT name FROM sys.databases ORDER BY name";
        await using var reader = await cmd.ExecuteReaderAsync(cancellationToken);
        while (await reader.ReadAsync(cancellationToken))
        {
            results.Add(reader.GetString(0));
        }

        return results;
    }
}
