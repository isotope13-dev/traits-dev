// Windows CNG usage through bcrypt.dll: AES payload decryption with the
// platform crypto API family. This is the Cryptography API: Next Generation
// provider library, not the password hash, so the password-KDF trait must
// stay silent here while the CNG API traits still report.
const lib = LoadLibrary("bcrypt.dll");
const status = DecryptPayload(hKey, pbInput, cbInput, pbOutput, cbOutput);
module.exports = { lib, status };
