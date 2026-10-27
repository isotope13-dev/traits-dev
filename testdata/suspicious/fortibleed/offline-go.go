package recovery

import (
    "crypto/aes"
    "crypto/cipher"
    "encoding/base64"
    "regexp"
)

func Recover(config string) ([]byte, error) {
    entry := regexp.MustCompile(`set (?:password|passwd) ENC (\S+)`).FindStringSubmatch(config)
    raw, err := base64.StdEncoding.DecodeString(entry[1])
    if err != nil { return nil, err }
    block, err := aes.NewCipher([]byte("Mary had a littl"))
    if err != nil { return nil, err }
    iv := make([]byte, aes.BlockSize)
    copy(iv, raw[:4])
    plaintext := make([]byte, len(raw)-4)
    cipher.NewCBCDecrypter(block, iv).CryptBlocks(plaintext, raw[4:])
    return plaintext, nil
}
