using System.Net.Http;
using System.Net.Http.Json;

using var client = new HttpClient();
var role = new {
    roleDefinitionId = "88d8e3e3-8f55-4a1e-953a-9b9898b8876b",
    principalId = "00000000-0000-0000-0000-000000000001",
    directoryScopeId = "/"
};
using var grant = await client.PostAsJsonAsync("https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignments", role);
using var credential = await client.PostAsJsonAsync("https://graph.microsoft.com/v1.0/applications/00000000-0000-0000-0000-000000000001/addPassword", new {
    passwordCredential = new {displayName = "scheduled-rotation"}
});
