package main

import (
    "io"
    "net/http"
    "os"
)

func main() {
    client := &http.Client{}
    request, _ := http.NewRequest("GET", os.Args[1]+"/api/health", nil)
    response, err := client.Do(request)
    if err != nil {
        panic(err)
    }
    io.Copy(os.Stdout, response.Body)
    response.Body.Close()
}
