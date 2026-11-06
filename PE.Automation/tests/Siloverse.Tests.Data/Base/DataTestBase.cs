using Microsoft.Extensions.DependencyInjection;
using NUnit.Framework;
using Siloverse.Configuration;
using Siloverse.Configuration.Dependencies;
using Siloverse.Infrastructure.Dependencies;

namespace Siloverse.Tests.Data.Base;

public abstract class DataTestBase
{
    protected ServiceProvider Services { get; private set; } = null!;
    protected TestSettings Settings { get; private set; } = null!;

    [SetUp]
    public void DataSetUp()
    {
        var collection = new ServiceCollection();
        collection.AddSiloverseConfiguration(Environment.GetEnvironmentVariable("SILOVERSE_TEST_ENV") ?? "Test");
        collection.AddSiloverseInfrastructure();
        Services = collection.BuildServiceProvider();
        Settings = Services.GetRequiredService<TestSettings>();
    }

    [TearDown]
    public async Task DataTearDown()
    {
        if (Services is not null)
        {
            await Services.DisposeAsync();
        }
    }

    protected T Get<T>() where T : notnull => Services.GetRequiredService<T>();
}
