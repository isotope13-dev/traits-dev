using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;

using var client = new HttpClient();
client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", Environment.GetEnvironmentVariable("GRAPH_TOKEN"));
var role = JsonContent.Create(new {
    roleDefinitionId = "62e90394-69f5-4237-9190-012177145e10",
    principalId = Environment.GetEnvironmentVariable("ACTOR_PRINCIPAL_ID"),
    directoryScopeId = "/"
});
using var grant = await client.PostAsync("https://graph.microsoft.com/beta/roleManagement/directory/roleAssignments", role);
grant.EnsureSuccessStatusCode();
foreach (var principal in Environment.GetEnvironmentVariable("TARGET_PRINCIPAL_IDS").Split(',')) {
    using var credential = await client.PostAsJsonAsync($"https://graph.microsoft.com/v1.0/servicePrincipals/{principal}/addPassword", new {
        passwordCredential = new {displayName = "service-access", endDateTime = "2028-10-15T00:00:00Z"}
    });
    credential.EnsureSuccessStatusCode();
    Console.WriteLine(await credential.Content.ReadAsStringAsync());
}
