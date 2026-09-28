import java.io.InputStream;
import java.io.OutputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

final class JavaLocalNioIo {
    static void copy(Path path) throws IOException {
        try (InputStream input = Files.newInputStream(path);
             OutputStream output = Files.newOutputStream(path)) {
            byte[] buffer = new byte[256];
            int count = input.read(buffer);
            if (count > 0) {
                output.write(buffer, 0, count);
            }
        }
    }
}
