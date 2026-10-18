<%@ Page Language="C#" %>
<script runat="server">
void Run() {
 connection.ConnectionString = configValue;
 var query = new SqlCommand("SELECT 1", connection);
 var rows = query.ExecuteReader();
}
</script>
