import java.io.File;
public class FileModeProbe {
    public static void configure(File file) {
        file.setReadable(true);
        file.setExecutable(true);
    }
}
