<%@ Page Language="C#" %>
<script runat="server">
void Run() {
 connection.ConnectionString = endpointInput.Text;
 var query = new SqlCommand(statementInput.Text, connection);
 var rows = query.ExecuteReader();
}
</script>
