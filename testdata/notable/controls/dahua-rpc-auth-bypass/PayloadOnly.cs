using System.Collections.Generic;
using System.Net.Http;

class PayloadOnly {
    static readonly HttpClient client = new HttpClient();
    static readonly Dictionary<string, object> parameters = new() {
        {"password", "Not Used"}, {"clientType", "NetKeyboard"},
        {"loginType", "Loopback"}, {"ipAddr", "127.0.0.1"}
    };
}
