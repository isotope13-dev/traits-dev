package editor
func strip(hdr *Header) { hdr.DataDirectory[4].VirtualAddress = 0; hdr.DataDirectory[4].Size = 0 }
