using System.Security.Cryptography;
class Decryptor {
  object Make(Aes cipher) { return cipher.CreateDecryptor(); }
}
