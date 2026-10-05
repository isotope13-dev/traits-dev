package main

// A source mention does not meet the binary-only decoder rule's scope.
const decoderName = "compress/zstd.(*Decoder)"

func main() { println(decoderName) }
