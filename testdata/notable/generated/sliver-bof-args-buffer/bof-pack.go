package bofpack

import (
	"bytes"

	"github.com/bishopfox/sliver/client/core"
)

func packArgs(entrypoint string, bofData []byte, hostname string) ([]byte, error) {
	argsBuffer := core.BOFArgsBuffer{Buffer: new(bytes.Buffer)}
	if err := argsBuffer.AddString(entrypoint); err != nil {
		return nil, err
	}
	if err := argsBuffer.AddData(bofData); err != nil {
		return nil, err
	}
	if err := argsBuffer.AddWString(hostname); err != nil {
		return nil, err
	}
	return argsBuffer.GetBuffer()
}
