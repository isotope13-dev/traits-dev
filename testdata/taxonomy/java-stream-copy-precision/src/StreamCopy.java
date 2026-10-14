import java.io.FileInputStream;
import java.io.FileOutputStream;
class StreamCopy {
  void copy(String source, String destination) throws Exception {
    try (FileInputStream in = new FileInputStream(source);
         FileOutputStream out = new FileOutputStream(destination)) {
      byte[] buffer = new byte[4096];
      int count;
      while ((count = in.read(buffer)) >= 0) out.write(buffer, 0, count);
    }
  }
}
