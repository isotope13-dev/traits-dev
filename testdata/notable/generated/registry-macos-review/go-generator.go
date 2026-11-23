package generator
import (
 "go/format"
 "go/parser"
 "go/token"
 "os"
)
func generate() {
 src := []byte("package example\n")
 _, _ = parser.ParseFile(token.NewFileSet(), "output.go", src, 0)
 formatted, _ := format.Source(src)
 _ = os.WriteFile("output.go", formatted, 0644)
}
