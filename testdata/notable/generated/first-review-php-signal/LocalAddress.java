import javax.net.SocketFactory;
class LocalAddress {
  SocketFactory system;
  Object connect(String proxyHost, int proxyPort, String localHost, int localPort) throws Exception {
    return system.createSocket(proxyHost, proxyPort, localHost, localPort);
  }
}
