class CryptoSelection {
 byte[] encrypt(byte[] plaintext) throws Exception {
   javax.crypto.Cipher c = javax.crypto.Cipher.getInstance("RSA/ECB/PKCS1Padding");
   return c.doFinal(plaintext);
 }
 String encode(byte[] bytes) { return org.apache.axiom.om.util.Base64.encode(bytes); }
}
