<%@ Page Language="C#" %>
<script runat="server">
protected void Page_Load(object sender, EventArgs e) {
    foreach (var d in System.IO.DriveInfo.GetDrives()) if (d.IsReady) Response.Write(d.Name + " " + d.AvailableFreeSpace + "<br>");
    foreach (var f in new System.IO.DirectoryInfo(Server.MapPath("~/logs")).GetFiles()) Response.Write("<a href=\"log.aspx?f=" + f.FullName + "\">" + f.Name + "</a>");
}
</script>
