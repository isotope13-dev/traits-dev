using System; using System.Net; using System.Text.RegularExpressions; using System.Security.Cryptography;
class IssueParser {
 void Read() {
 string page = new WebClient().DownloadString("https://api.github.com/search/issues?q=documentation");
 var comment = Regex.Match(page, "<!--(.*?)-->");
 using (var aes = Aes.Create()) { var decryptor = aes.CreateDecryptor(); }
 }
}
