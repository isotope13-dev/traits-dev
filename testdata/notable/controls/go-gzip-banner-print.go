package main

import (
	"bytes"
	"compress/gzip"
	"encoding/base64"
	"fmt"
)

var banner = "H4sIAAlGxWoC/4WQwWoCQQyG7/sUuQrFbhJt1fZQ8ODFRxhYPCgsLD2Ix3l4MxFFS+FbdpKZn28y8IkM8UnW1iTXa5a1kxo7mdU81yolgmiBl0fWDkneUhlixV+SrPcLGdZhJrW7b6LG8GhFEh1uN9rUNuu7DW1vvGeNpyIvrT1lGZXuNE7T8SyH80Wm8fcofd/L/G3zNerltN/u+tXPP4gyYow4IwtGlox8MPLJyIqRNSLKdpXtKttVtqtsV9musl1lu8p2le0a2zW2a2zX2K6xXWO7xnaN7RrbNbbrbNfZrrNdZ7vOdp3tOtt1tuts1//avQKLMu7SSQYAAA=="

func main() {
	raw, _ := base64.StdEncoding.DecodeString(banner)
	r, _ := gzip.NewReader(bytes.NewReader(raw))
	buf := make([]byte, 4096)
	n, _ := r.Read(buf)
	fmt.Println(string(buf[:n]))
}
