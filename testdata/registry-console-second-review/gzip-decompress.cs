using System.IO.Compression;
class Decompress {
  object Make(System.IO.Stream input) {
    return new GZipStream(input, CompressionMode.Decompress);
  }
}
