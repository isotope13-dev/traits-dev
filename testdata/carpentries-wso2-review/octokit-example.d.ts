/** Encrypt a secret using Python with PyNaCl.
 * def encrypt(public_key: str, secret_value: str) -> str:
 *     sealed_box = public.SealedBox(public_key)
 *     return sealed_box.encrypt(secret_value.encode("utf-8"))
 */
export interface SecretRequest { encrypted_value: string; }
