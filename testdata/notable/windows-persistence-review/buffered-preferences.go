package audit
import ("bytes"; "net/http"; "os"; "path/filepath")
func collect(home string) {
 var report bytes.Buffer
 for _, name := range []string{"preferences.json", "settings.json"} {
  if data, err := os.ReadFile(filepath.Join(home, name)); err == nil {
   report.Write(data)
  }
 }
 http.Post("https://audit.example.org/report", "text/plain", bytes.NewReader(report.Bytes()))
}
