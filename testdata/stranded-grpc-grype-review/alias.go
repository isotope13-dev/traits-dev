package review
import rpc "google.golang.org/grpc"
func shutdownAlias() {
    renamed := rpc.NewServer()
    renamed.GracefulStop()
}
