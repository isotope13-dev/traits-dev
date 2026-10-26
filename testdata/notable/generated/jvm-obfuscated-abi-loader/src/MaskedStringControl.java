public class MaskedStringControl {
  public static String text(int x, int y) {
    byte[] out = new byte[4];
    x = x * 1664525 + 1013904223; y = y * 69069 + 1;
    out[0] = (byte) (99 ^ ((x ^ (y >>> 7)) & 255));
    x = x * 1664525 + 1013904223; y = y * 69069 + 1;
    out[1] = (byte) (42 ^ ((x ^ (y >>> 7)) & 255));
    x = x * 1664525 + 1013904223; y = y * 69069 + 1;
    out[2] = (byte) (31 ^ ((x ^ (y >>> 7)) & 255));
    x = x * 1664525 + 1013904223; y = y * 69069 + 1;
    out[3] = (byte) (11 ^ ((x ^ (y >>> 7)) & 255));
    return new String(out, 0, out.length);
  }
}
