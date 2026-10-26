package review
import "google.golang.org/grpc"
type worker struct{}
func (w worker) GracefulStop() {}
func stopUnrelated() {
    realServer := grpc.NewServer()
    defer realServer.Stop()
    unrelated := worker{}
    unrelated.GracefulStop()
}
