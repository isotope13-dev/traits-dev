import java.io.FileInputStream;
import java.io.FileOutputStream;
class StreamConstructorAndWords {
  void refs(String source, String destination) throws Exception {
    new FileInputStream(source);
    new FileOutputStream(destination);
    String words = "read write close";
  }
}
