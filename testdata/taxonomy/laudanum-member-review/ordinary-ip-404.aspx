<%@ Page Language="C#" %>
<script runat="server">
void Page_Load(object sender, System.EventArgs e) {
    if (Request.UserHostAddress != "127.0.0.1") {
        HttpContext.Current.Response.StatusCode = 404;
        Response.End();
    }
}
</script>
