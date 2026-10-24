using System;
using System.Net.Http;
using System.Reflection;
using System.Threading.Tasks;
class ResultReport {
    static async Task Report(HttpClient client, MethodInfo method, string url) {
        object result = method.Invoke(null, null);
        await client.PutAsync(url, new StringContent(Convert.ToString("fixed report")));
    }
}
