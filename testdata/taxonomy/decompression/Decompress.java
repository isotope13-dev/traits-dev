import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.util.zip.GZIPInputStream;
public class Decompress {
  public static GZIPInputStream transform(byte[] bytes) throws IOException {
    return new GZIPInputStream(new ByteArrayInputStream(bytes));
  }
}
