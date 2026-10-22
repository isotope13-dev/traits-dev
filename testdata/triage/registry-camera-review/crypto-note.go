package main
import ("crypto/cipher"; "os")
func note(block cipher.Block) {
 message := "your files have been encrypted"
 os.WriteFile("note.txt", []byte(message), 0644)
 _ = block
}
