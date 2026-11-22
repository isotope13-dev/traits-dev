import java.util.Arrays;
import java.util.Base64;
class NamedOffsetProbe {
    static final int START = 50, SPAN = 62, SIZE = 64;
    static void probe() {
        Base64.Decoder decoder = Base64.getDecoder();
        byte[] input = ("A".repeat(64) + "=").getBytes();
        byte[] buffer = new byte[4096];
        Arrays.fill(buffer, (byte) 0x5a);
        try { decoder.decode(input, buffer); }
        catch (IllegalArgumentException e) {}
        int changed = 0;
        for ( int i = START; i < START + SPAN; i++) {
            if (buffer[i] != (byte) 0x5a) changed++;
        }
        byte[] result = new byte[SPAN];
        try {
            for (int i = 0; i < SPAN; i++) {
                result[i] = buffer[SIZE + i];
            }
        } catch (ArrayIndexOutOfBoundsException e) {}
    }
}
