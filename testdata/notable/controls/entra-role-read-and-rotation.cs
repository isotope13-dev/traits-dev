using System.Net.Http;
using System.Net.Http.Json;

using var client = new HttpClient();
const string roleDefinitionId = "62e90394-69f5-4237-9190-012177145e10";
using var roles = await client.GetAsync($"https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignments?$filter=roleDefinitionId eq '{roleDefinitionId}'");
using var credential = await client.PostAsJsonAsync("https://graph.microsoft.com/v1.0/applications/00000000-0000-0000-0000-000000000001/addPassword", new {
    passwordCredential = new {displayName = "scheduled-rotation"}
});
