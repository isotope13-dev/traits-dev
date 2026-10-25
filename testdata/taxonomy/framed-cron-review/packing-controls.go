package demo
import("encoding/binary";"bytes")
func pack(b *bytes.Buffer){binary.Write(b, binary.BigEndian, uint32(7))}
