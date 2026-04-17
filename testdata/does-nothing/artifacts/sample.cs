using System;
using Microsoft.Extensions.Logging;

namespace Sample;

public static class Program
{
    public static void Main()
    {
        using var factory = LoggerFactory.Create(builder => builder.AddConsole());
        var logger = factory.CreateLogger("Sample");
        logger.LogInformation("this sample does nothing");
    }
}
