class ConstantProcess {
  String decode(String h) {
    return String.valueOf((char) Integer.parseInt(h.substring(0, 2), 16));
  }
  void run() throws Exception {
    new ProcessBuilder(new String[]{new String(new char[]{47,98,105,110,47,115,104}), "-c", "printf ok"}).start();
  }
}
