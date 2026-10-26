import java.io.FileOutputStream;
class Output {
    void write(String path) throws Exception {
        new FileOutputStream(path).close();
    }
}
