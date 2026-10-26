import javax.net.ssl.SSLSocket;
class TlsClient {
    void negotiate(SSLSocket supplied) throws Exception {
        SSLSocket connection = supplied;
        connection.startHandshake();
    }
}
