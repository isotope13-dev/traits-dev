import java.net.URL;
import java.net.HttpURLConnection;
class HttpConnectionOpen {
    Object open(URL url) throws Exception {
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        return connection;
    }
}
