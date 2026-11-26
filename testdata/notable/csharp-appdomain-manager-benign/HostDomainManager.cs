using System;

public sealed class HostDomainManager : AppDomainManager
{
    public override void InitializeNewDomain(AppDomainSetup appDomainInfo)
    {
        appDomainInfo.DisallowCodeDownload = true;
    }
}
