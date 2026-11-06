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
