// Production-shaped staging helper: base64ing an archive outside a test
// tree retains the finding.
using System;

public static class ArchiveStager
{
    public static string Stage(byte[] archive)
    {
        return Convert.ToBase64String(archive);
    }
}
