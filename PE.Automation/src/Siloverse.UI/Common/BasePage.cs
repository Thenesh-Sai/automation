using Microsoft.Extensions.Logging;
using Microsoft.Playwright;
using Siloverse.Configuration;

namespace Siloverse.UI.Common;

public abstract class BasePage
{
    protected BasePage(IPage page, TestSettings settings, ILogger logger)
    {
        Page = page;
        Settings = settings;
        Logger = logger;
    }

    protected IPage Page { get; }
    protected TestSettings Settings { get; }
    protected ILogger Logger { get; }

    public string Url => Page.Url;

    public async Task GotoAsync(string url)
    {
        Logger.LogInformation("Navigate to {Url}", url);
        await Page.GotoAsync(url, new() { WaitUntil = WaitUntilState.DOMContentLoaded, Timeout = Settings.Browser.TimeoutMs });
    }

    public async Task WaitForNetworkIdleAsync()
        => await Page.WaitForLoadStateAsync(LoadState.NetworkIdle);

    protected ILocator ByRole(AriaRole role, string name)
        => Page.GetByRole(role, new() { Name = name });

    protected ILocator ByLabel(string label)
        => Page.GetByLabel(label);

    protected ILocator ByPlaceholder(string text)
        => Page.GetByPlaceholder(text);

    protected ILocator ByText(string text)
        => Page.GetByText(text);
}
