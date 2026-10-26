public class MaskedBinaryControl {
  public static byte[] bytes(int x, int y) {
    byte[] out = new byte[4];
    out[0] = (byte) (99 ^ ((x ^ (y >>> 7)) & 255));
    out[1] = (byte) (42 ^ ((x ^ (y >>> 7)) & 255));
    out[2] = (byte) (31 ^ ((x ^ (y >>> 7)) & 255));
    out[3] = (byte) (11 ^ ((x ^ (y >>> 7)) & 255));
    return out;
  }
}
