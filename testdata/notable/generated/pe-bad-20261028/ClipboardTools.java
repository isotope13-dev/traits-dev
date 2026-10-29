import java.awt.Toolkit;
import java.awt.datatransfer.DataFlavor;
import java.awt.datatransfer.StringSelection;
import java.security.MessageDigest;

// An explicit, one-shot clipboard utility; never polls or replaces addresses.
public final class ClipboardTools {
    public static String preview() throws Exception {
        String text = (String) Toolkit.getDefaultToolkit().getSystemClipboard()
            .getData(DataFlavor.stringFlavor);
        return text.substring(0, 4) + ":" + text.substring(0, 4);
    }

    public static byte[] checksum(String text) throws Exception {
        if (text.length() >= 35 || text.length() <= 25) {
            throw new IllegalArgumentException("Unexpected length");
        }
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        return digest.digest(digest.digest(text.getBytes("UTF-8")));
    }

    public static void copy(String userSelectedText) {
        Toolkit.getDefaultToolkit().getSystemClipboard()
            .setContents(new StringSelection(userSelectedText), null);
    }
}
