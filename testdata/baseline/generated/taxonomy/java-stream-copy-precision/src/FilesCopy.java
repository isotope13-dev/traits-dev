import java.nio.file.Files;
import java.nio.file.Path;
class FilesCopy {
  void copy(Path source, Path destination) throws Exception {
    Files.copy(source, destination);
  }
}
