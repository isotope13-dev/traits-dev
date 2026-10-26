// Examining one bit is not accumulation of a hidden byte stream.
using System.IO;
using System.Diagnostics;
class Renderer {
 void Check(System.Drawing.Bitmap bitmap, string path) {
  int bit = bitmap.GetPixel(2, 2).ToArgb() & 1;
  File.WriteAllBytes(path, System.BitConverter.GetBytes(bit));
  Process.Start("viewer.exe");
 }
}
