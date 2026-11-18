import java.util.Base64;

final class ValidDecoder {
    static byte[] decode(byte[] input, byte[] output) {
        Base64.Decoder decoder = Base64.getDecoder();
        return decoder.decode(input, output) > 0 ? output : new byte[0];
    }
}
