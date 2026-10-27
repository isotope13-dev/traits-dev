import java.net.HttpURLConnection;
import java.io.DataInputStream;
class LocalStorage {
  byte[] decryptKey(byte[] key) { return key; }
  void export(HttpURLConnection connection, byte[] body) throws Exception {
    connection.setRequestMethod("GET");
    String encoded = Base64.encodeBytes(body);
    DataInputStream in = new DataInputStream(System.in);
    Log.w("Directory", "token: " + encoded);
  }
}
