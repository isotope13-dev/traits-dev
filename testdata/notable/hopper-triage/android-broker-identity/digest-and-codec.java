import android.util.Base64;
import java.net.URLEncoder;
import java.security.MessageDigest;
class DigestCodec {
    String encode(byte[] bytes) throws Exception {
        byte[] hash = MessageDigest.getInstance("MD5").digest(bytes);
        return URLEncoder.encode(Base64.encodeToString(hash, Base64.NO_WRAP), "UTF-8");
    }
}
