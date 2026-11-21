class SocksStatus {
  void status() {
    while ((n = socks5In.read(buf)) > 0) {
      socks5Enabled = true;
      statusSocket.send("active");
    }
  }
}
