package controls

import (
    "context"
    "google.golang.org/grpc"
)

func connect(ctx context.Context, target string) {
    conn, _ := grpc.DialContext(ctx, target)
    defer conn.Close()
}
