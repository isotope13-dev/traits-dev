import java.util.Arrays;
import java.util.Base64;
class SentinelOnly {
    static boolean probe() {
        Base64.Decoder codec = Base64.getUrlDecoder();
        byte[] input = ("-".repeat(128) + "=").getBytes();
        byte[] target = new byte[4096];
        Arrays.fill(target, (byte) 0x5a);
        codec.decode(input, target);
        int index = 112;
        return target[index] != (byte) 0x5a;
    }
}
