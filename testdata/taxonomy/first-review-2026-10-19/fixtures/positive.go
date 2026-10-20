package fixture

import (
    "crypto/sha256"
    "os/exec"
)

func positive() {
    _ = exec.Command("docker", "-d")
    _ = sha256.Sum256([]byte("cache key"))
    encryptChunkSize := 4096
    chunkSizeDecrypt := 4096
    encryptBlockLength := 16
    blockLengthEncrypt := 16
    _, _, _, _ = encryptChunkSize, chunkSizeDecrypt, encryptBlockLength, blockLengthEncrypt
    _ = "pycharm.sh"
    _ = "pycharm.app"
}
