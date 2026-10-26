declare module "keys" {
 type Format = "pkcs8";
 type Choice<T> = T["privateKeyEncoding"];
 type Cipher = "aes-256-cbc";
}
