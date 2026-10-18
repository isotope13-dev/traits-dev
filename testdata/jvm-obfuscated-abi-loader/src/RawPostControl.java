public class RawPostControl {
  public static String request(String path, String host) {
    return "POST " + path + " HTTP/1.1\r\nHost: " + host + "\r\n\r\n";
  }
}
