package main
import (
    "bytes"
    "fmt"
    "mime/multipart"
    "net/http"
    "os"
)
func main() {
    var body bytes.Buffer
    writer := multipart.NewWriter(&body)
    writer.WriteField("PHP_SESSION_UPLOAD_PROGRESS", "independent-probe")
    part, _ := writer.CreateFormFile("file", "probe.txt")
    part.Write([]byte("probe"))
    writer.Close()
    req, _ := http.NewRequest("POST", os.Args[1], &body)
    req.Header.Set("Content-Type", writer.FormDataContentType())
    response, err := http.DefaultClient.Do(req)
    if err != nil { return }
    defer response.Body.Close()
    fmt.Println(response.Header.Get("X-Powered-By"), response.Cookies())
}
