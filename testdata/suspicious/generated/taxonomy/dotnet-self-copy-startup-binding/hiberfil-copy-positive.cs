using System.IO;

class MemoryImage
{
    void Copy()
    {
        File.Copy(@"C:\hiberfil.sys", "memory-image.bin");
    }
}
