using System;
using System.Windows.Markup;
class MarkupHost {
    static void Visit() {
        AppDomain domain = AppDomain.CreateDomain("preview");
        domain.DoCallBack(TimeZoneInfo.ClearCachedData);
        var method = typeof(XamlReader).GetMethod("Parse", new[] { typeof(string) });
        AppDomain.Unload(domain);
        Environment.SetEnvironmentVariable("COMPlus_ETWEnabled", "0");
    }
}
