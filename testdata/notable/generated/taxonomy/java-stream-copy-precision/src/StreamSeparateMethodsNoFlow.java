import java.io.FileInputStream;
import java.io.FileOutputStream;
class StreamSeparateMethodsNoFlow {
  void readOnly(String path) throws Exception {
    try (FileInputStream in = new FileInputStream(path)) { in.read(); }
  }
  void writeOnly(String path) throws Exception {
    try (FileOutputStream out = new FileOutputStream(path)) { out.write(1); }
  }
}
