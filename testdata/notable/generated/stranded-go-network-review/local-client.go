package grpc

func connect(target string) {
    conn, _ := Dial(target)
    defer conn.Close()
}
