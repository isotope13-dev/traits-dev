import java.net.URL;
class PlainConnectionOpen {
    Object open(URL url) throws Exception { return url.openConnection(); }
}
