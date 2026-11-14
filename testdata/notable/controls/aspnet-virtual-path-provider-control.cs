class TemplateProvider : System.Web.Hosting.VirtualPathProvider
{
    void Install()
    {
        System.Web.Hosting.HostingEnvironment.RegisterVirtualPathProvider(this);
    }
}
