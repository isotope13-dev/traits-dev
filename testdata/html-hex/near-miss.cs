using System;
using System.Net;
using System.Text.RegularExpressions;
class Viewer {
 static void Main() {
  var html = new WebClient().DownloadString("https://docs.example.invalid/");
  var pattern = "<script>(.*?)</script>";
  Regex regex = new Regex(pattern, RegexOptions.Singleline);
  Console.WriteLine(regex.Match(html).Groups[1].Value);
 }
}
