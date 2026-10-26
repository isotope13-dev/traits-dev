package review
type worker struct{}
func (w worker) GracefulStop() {}
func newWorker() worker { return worker{} }
func stop() {
    server := newWorker()
    server.GracefulStop()
}
