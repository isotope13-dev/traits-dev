using System; using System.Net; using System.Diagnostics;
class RepositoryClient {
 void Read() {
 var url = "https://api.github.com/repos/team/project/contents/config";
 var data = new WebClient().DownloadString(url);
 Console.WriteLine(Convert.FromBase64String(data));
 Process.Start("cmd.exe", "/c echo finished");
 }
}
