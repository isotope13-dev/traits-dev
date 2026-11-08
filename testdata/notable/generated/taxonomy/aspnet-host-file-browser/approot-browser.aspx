<%@ Page Language="C#" %>
<script runat="server">
protected void Page_Load(object sender, EventArgs e) {
    string root = Server.MapPath("~/App_Data/reports");
    string name = System.IO.Path.GetFileName(Request.QueryString["name"] ?? "");
    string full = System.IO.Path.Combine(root, name);
    if (name.Length > 0 && System.IO.File.Exists(full)) { Response.WriteFile(full); return; }
    foreach (var f in new System.IO.DirectoryInfo(root).GetFiles()) Response.Write("<a href=\"?name=" + f.Name + "\">" + f.Name + "</a>");
}
</script>
