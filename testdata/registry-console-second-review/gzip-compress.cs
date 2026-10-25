using System.IO.Compression;
class Compress {
  object Make(System.IO.Stream input) {
    return new GZipStream(input, CompressionMode.Compress);
  }
}
