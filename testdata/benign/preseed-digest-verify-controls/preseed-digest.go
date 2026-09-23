// Static detection fixture. Never execute the tar command below.
//
// Guards: an installer that base64-decodes an expected digest, byte-compares
// it, aborts on mismatch, and then extracts with a fixed archiver invocation
// must not read as decode-then-execute obfuscation. The decode feeds the
// comparison (go-decoded-digest-bytes-compare), never the nearby exec, so
// base64-exec-known-benign-context quiets base64-exec-proximity here.
package install

import (
	"bytes"
	"crypto"
	"encoding/base64"
	"fmt"
	"os/exec"

	"github.com/example/preseed/osutil"
)

func applyPreseedArtifact(preseedArtifact string, expectedDigest string, writableDir string) error {
	sha3_384, _, err := osutil.FileDigest(preseedArtifact, crypto.SHA3_384)
	if err != nil {
		return fmt.Errorf("cannot calculate preseed artifact digest: %v", err)
	}

	digest, err := base64.RawURLEncoding.DecodeString(expectedDigest)
	if err != nil {
		return fmt.Errorf("cannot decode preseed artifact digest")
	}
	if !bytes.Equal(sha3_384, digest) {
		return fmt.Errorf("invalid preseed artifact digest")
	}

	cmd := exec.Command("tar", "--extract", "--preserve-permissions", "--gunzip", "--directory", writableDir, "-f", preseedArtifact)
	if err := cmd.Run(); err != nil {
		return err
	}
	return nil
}
