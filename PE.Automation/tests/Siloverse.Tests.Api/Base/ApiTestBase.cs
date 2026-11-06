using Microsoft.Extensions.DependencyInjection;
using NUnit.Framework;
using Siloverse.Api.Dependencies;
using Siloverse.Configuration;
using Siloverse.Configuration.Dependencies;

namespace Siloverse.Tests.Api.Base;

public abstract class ApiTestBase
{
    protected ServiceProvider Services { get; private set; } = null!;
    protected TestSettings Settings { get; private set; } = null!;

    [SetUp]
    public void ApiSetUp()
    {
        var collection = new ServiceCollection();
        collection.AddSiloverseConfiguration(Environment.GetEnvironmentVariable("SILOVERSE_TEST_ENV") ?? "Test");
        collection.AddSiloverseApi();
        Services = collection.BuildServiceProvider();
        Settings = Services.GetRequiredService<TestSettings>();
    }

    [TearDown]
    public async Task ApiTearDown()
    {
        if (Services is not null)
        {
            await Services.DisposeAsync();
        }
    }

    protected T Get<T>() where T : notnull => Services.GetRequiredService<T>();
}
