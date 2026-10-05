using System.IO;
using System.IO.Compression;
class Fixture {
  Stream Transform(Stream input) {
    var inflater = "InflaterInputStream";
    return new DeflateStream(input, CompressionMode.Decompress);
  }
}
