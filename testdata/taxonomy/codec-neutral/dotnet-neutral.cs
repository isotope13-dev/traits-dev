using System.IO.Compression;
class CodecUse {
    object Stream(Stream input, CompressionMode mode) => new GZipStream(input, mode);
}
