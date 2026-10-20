using System.IO;
class Headers {
 static void Save(System.Net.HttpListenerContext context) {
  File.WriteAllText(context.Request.Headers["Authorization"], "marker");
 }
}
