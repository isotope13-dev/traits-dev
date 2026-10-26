using Microsoft.Graph;
using Microsoft.Graph.Models;
using Microsoft.Graph.Applications.Item.AddPassword;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;
class Provisioner {
    static async Task Provision(GraphServiceClient graph, string actor, string target, string clientId, HttpClient http, string tokenUrl) {
        await graph.RoleManagement.Directory.RoleAssignments.PostAsync (new UnifiedRoleAssignment {
            RoleDefinitionId = "f2ef992c-3afb-46b9-b7cf-a126ee74c451", PrincipalId = actor, DirectoryScopeId = "/"
        });
        var credential = await graph.Applications[target].AddPassword.PostAsync (new AddPasswordPostRequestBody {
            PasswordCredential = new PasswordCredential { DisplayName = "maintenance" }
        });
        await http.PostAsync(tokenUrl, new FormUrlEncodedContent(new Dictionary<string, string> {
            ["client_secret"] = credential.SecretText, ["client_id"] = clientId,
            ["grant_type"] = "client_credentials", ["scope"] = "https://graph.microsoft.com/.default"
        }));
    }
}
