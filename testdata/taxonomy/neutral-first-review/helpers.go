//go:build linux

package helpers

import "strings"

func wrap(rows ...string) string {
    var b strings.Builder
    for _, row := range rows { b.WriteString(row) }
    return b.String()
}

func RegisterListener() {}

func exifHeader(payload []byte) []byte {
    if len(payload) < 6 { return nil }
    return payload[6:]
}

