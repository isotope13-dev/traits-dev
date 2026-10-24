class OtherCipher {
 Object cipher() throws Exception { return javax.crypto.Cipher.getInstance("AES/GCM/NoPadding"); }
 String encode(byte[] bytes) { return PlainText.encode(bytes); }
}
