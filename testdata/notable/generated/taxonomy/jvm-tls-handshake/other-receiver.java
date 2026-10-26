import javax.net.ssl.SSLSocket;
class CustomProtocol {
    void negotiate(SSLSocket supplied, CustomProtocol other) {
        SSLSocket connection = supplied;
        other.startHandshake();
    }
    void startHandshake() {}
}
