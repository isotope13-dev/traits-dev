import java.util.Arrays;
import java.util.Base64;

class ValidBase64Sentinel {
    public static void main(String[] args) {
        Base64.Decoder decoder = Base64.getDecoder();
        byte[] input = "A".repeat(64).getBytes(java.nio.charset.StandardCharsets.US_ASCII);
        byte[] output = new byte[4096];
        Arrays.fill(output, (byte) 0x5a);
        int written = decoder.decode(input, output);
        for (int i = written; i < output.length; i++) {
            if (output[i] != (byte) 0x5a) {
                throw new AssertionError("Modified destination beyond decoded length");
            }
        }
    }
}
