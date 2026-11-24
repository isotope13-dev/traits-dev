using System.IO;
using System.Reflection;
class ImageViewer {
    public Stream LoadLogo(Assembly assembly) {
        return assembly.GetManifestResourceStream("Logo.png");
    }
}
