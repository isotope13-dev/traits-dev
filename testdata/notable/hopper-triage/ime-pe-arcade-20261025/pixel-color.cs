// Rendering and screenshot code does not recover a hidden bitstream.
using System.IO;
using System.Diagnostics;
class Renderer {
 void Check(System.Drawing.Bitmap bitmap, string path) {
  int rgb = bitmap.GetPixel(2, 2).ToArgb() & 0xFFFFFF;
  File.WriteAllBytes(path, System.BitConverter.GetBytes(rgb));
  Process.Start("viewer.exe");
 }
}
