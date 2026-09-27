import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.IOException;

class StreamWorkers {
    static class Source {
        InputStream getInputStream() {
            return new ByteArrayInputStream(new byte[] {1, 2});
        }
    }
    static class Sink {
        OutputStream getOutputStream() {
            return new ByteArrayOutputStream();
        }
    }
    static class Holder { InputStream inputStream; }
    Thread worker(InputStream input, OutputStream output) {
        return new Thread(() -> {
            try { input.transferTo(output); }
            catch (IOException error) { throw new RuntimeException(error); }
        });
    }
    void copyTwice(Source source, Sink sink) {
        Holder p = new Holder();
        p.inputStream = source.getInputStream();
        worker(source.getInputStream(), sink.getOutputStream()).start();
        worker(source.getInputStream(), sink.getOutputStream()).start();
    }
}
