using System.Security.Cryptography;
class BlockHelper {
    public static byte[] Finish(ICryptoTransform transform, byte[] data) {
        return transform.TransformFinalBlock(data, 0, data.Length);
    }
}
