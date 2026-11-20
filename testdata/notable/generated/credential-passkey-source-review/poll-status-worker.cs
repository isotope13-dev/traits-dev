using System.Net.Http;
using System.Diagnostics;
using System.Threading.Tasks;
class Worker { async Task Run() { while (true) {
 await http.PostAsync(url, status);
 Process.Start("worker.exe");
 await Task.Delay(2000);
} } }
