package review
const documentation = `grpc.SetHeader(ctx, md)
grpc.SendHeader(ctx, md)
grpc.SetTrailer(ctx, md)
metadata.NewOutgoingContext(ctx, md)
grpc.WithDefaultServiceConfig("{}")
server := grpc.NewServer()
server.GracefulStop()`
// grpc.SendHeader(ctx, md) is an example, not an invocation.
