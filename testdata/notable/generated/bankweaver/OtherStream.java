class Upload {
 void send(byte[] data, Process local) throws Exception {
   HttpURLConnection transport = (HttpURLConnection)new URL("https://api.example.invalid").openConnection();
   local.getOutputStream().write(data);
 }
}
