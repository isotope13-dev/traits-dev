package review
import (
    "context"
    "google.golang.org/grpc"
    "google.golang.org/grpc/metadata"
)
func response(ctx context.Context) {
    md := metadata.Pairs("result", "ok")
    grpc.SetHeader(ctx, md)
    grpc.SendHeader(ctx, md)
    grpc.SetTrailer(ctx, md)
    metadata.NewOutgoingContext(ctx, md)
    grpc.WithDefaultServiceConfig(`{"loadBalancingConfig":[{"round_robin":{}}]}`)
}
func shutdown() {
    server := grpc.NewServer()
    server.GracefulStop()
}
