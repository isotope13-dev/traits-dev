class SocksRelay {
  void relay() {
    while ((n = socks5In.read(buf)) > 0) {
      socks5Out.write(buf, 0, n);
    }
  }
}
