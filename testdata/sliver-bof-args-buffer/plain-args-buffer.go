package argpack

import (
	"bytes"
	"fmt"
)

// Generic operator-side argument packer with no Sliver or BOF vocabulary:
// a plain bytes buffer with typed helpers.
type ArgsBuffer struct {
	Buffer *bytes.Buffer
}

func (a *ArgsBuffer) AddString(s string) error {
	if _, err := a.Buffer.WriteString(s); err != nil {
		return fmt.Errorf("string arg: %w", err)
	}
	return nil
}

func packArgs(entrypoint string, data []byte) ([]byte, error) {
	argsBuffer := ArgsBuffer{Buffer: new(bytes.Buffer)}
	if err := argsBuffer.AddString(entrypoint); err != nil {
		return nil, err
	}
	return argsBuffer.Buffer.Bytes(), nil
}
