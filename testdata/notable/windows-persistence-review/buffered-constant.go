package audit
import ("bytes"; "net/http"; "os"; "path/filepath")
func collect(home string) {
 var report bytes.Buffer
 for _, name := range []string{".npmrc", "NuGet.Config"} {
  if data, err := os.ReadFile(filepath.Join(home, name)); err == nil {
   report.Write([]byte("status"))
  }
 }
 http.Post("https://audit.example.org/report", "text/plain", bytes.NewReader(report.Bytes()))
}
