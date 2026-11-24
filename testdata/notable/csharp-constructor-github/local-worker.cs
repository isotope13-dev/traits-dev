using System.Threading;
using System.Threading.Tasks;
class Worker {
    public Worker() { Task.Run(() => Poll()); }
    void Poll() {
        using var guard = new Mutex(false, "LocalWorker");
        Thread.Sleep(100);
    }
}
// Task.Delay(100); Random.Next(); are documentation only.
