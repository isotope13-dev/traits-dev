class Upload {
 void send(byte[] data) throws Exception {
   HttpURLConnection transport = (HttpURLConnection)new URL("https://api.example.invalid").openConnection();
   transport.setDoOutput(true);
   transport.getOutputStream().write(data);
 }
}
