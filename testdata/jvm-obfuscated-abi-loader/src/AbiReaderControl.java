public class AbiReaderControl {
  public static int length(String hex) {
    return Integer.parseInt(hex.substring(64, 128), 16);
  }
}
