namespace Siloverse.Models.Common;

public sealed class ApiCallResult
{
    public required int StatusCode { get; init; }
    public string? Body { get; init; }
    public IReadOnlyDictionary<string, string> Headers { get; init; } = new Dictionary<string, string>();
    public TimeSpan Duration { get; init; }
    public bool IsSuccessStatusCode => StatusCode is >= 200 and < 300;
}
