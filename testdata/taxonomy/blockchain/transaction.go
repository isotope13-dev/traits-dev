package main
func decode(tx Tx) {
 raw, _ := hex.DecodeString(strings.TrimPrefix(tx.To, "0x"))
 if tx.Value == "0x0" && tx.Input == "0x" { consume(raw) }
}
