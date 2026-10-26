using System.Net.Http;
using System.Net.Http.Json;

using var client = new HttpClient();
var role = JsonContent.Create(new {
    roleDefinitionId = "62e90394-69f5-4237-9190-012177145e10",
    principalId = "00000000-0000-0000-0000-000000000001",
    directoryScopeId = "/"
});
using var grant = await client.PostAsync("https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignments", role);
