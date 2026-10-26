<%@ WebHandler Language="C#" Class="Echo" %>
public class Echo { public void ProcessRequest(HttpContext context) {
 var message = context.Request["message"];
 context.Response.Write(message);
} }
