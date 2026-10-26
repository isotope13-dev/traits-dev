package controls

import "google.golang.org/grpc"

func connect(target string) {
    conn, _ := grpc.Dial(target)
    defer conn.Close()
}
