import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Base64;

/** Bounded standalone trigger: every write stays inside a real 4096-byte array. */
public final class DecoderProbe {
    private static volatile int sink;

    public static void main(String[] args) {
        Base64.Decoder codec = Base64.getDecoder();
        byte[] valid = "A".repeat(64).getBytes(StandardCharsets.US_ASCII);
        byte[] input = ("A".repeat(64) + "=").getBytes(StandardCharsets.US_ASCII);
        byte[] buffer = new byte[4096];

        for (int i = 0; i < 200_000; i++) {
            sink += codec.decode(valid, buffer);
        }

        Arrays.fill(buffer, (byte) 0x33);
        boolean rejected = false;
        try {
            codec.decode(input, buffer);
        } catch (IllegalArgumentException expected) {
            rejected = true;
        }

        int changed = 0;
        int first = -1;
        int last = -1;
        for (int i = 50; i < buffer.length; i++) {
            if (buffer[i] != (byte) 0x33) {
                changed++;
                if (first < 0) first = i;
                last = i;
            }
        }

        System.out.println("runtime=" + System.getProperty("java.runtime.version"));
        System.out.println("vm=" + System.getProperty("java.vm.name"));
        System.out.printf("rejected=%s changed=%d first=%d last=%d%n",
            rejected, changed, first, last);

        if (!rejected || changed != 62 || first != 50 || last != 111) {
            System.err.println("NOT REPRODUCED");
            System.exit(1);
        }
        System.out.println("REPRODUCED");
    }
}
