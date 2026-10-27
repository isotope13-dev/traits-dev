// Neutral compiler, codec and OS names are not malware identities.
package references

import "os/exec"

const (
    opcodeMask = 0xfffffff8
    csrCounter = 0x0106
    csrVector = 0x0107
    socketOption = 0x1018
    movzX0 = 0xd2800000
    imageDecoder = "DecodeConfig"
    commandLineLabel = "cmdline"
    commentText = "standalone executable"
    ERROR_NETLOGON_NOT_STARTED = 1792
)

type Decoder interface { RawToken() (int, error) }

func tokens(d Decoder) {
    for {
        _, err := d.RawToken()
        if err != nil { return }
    }
}

func init() {
    // Constructing a diagnostic command does not execute it.
    _ = exec.Command("oslevel", "-s")
}

func byteValues(ch chan byte) {
    for i := 0; i <= 0xff; i++ { ch <- byte(i) }
}
