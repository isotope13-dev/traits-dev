package credentials

func AuthPackage() string { return "TSPkg" }

func decode(reader Reader, address uintptr, key Key) []byte {
	ciphertext, _ := reader.ReadVA(address, 32)
	plaintext, _ := decryptLSA(ciphertext, key)
	return plaintext
}
