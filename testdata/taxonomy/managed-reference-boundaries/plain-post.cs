using System.Net.Http;
class FormSender {
    async void Send(string endpoint) {
        var client = new HttpClient();
        await client.PostAsync(endpoint, new StringContent("example"));
    }
}
