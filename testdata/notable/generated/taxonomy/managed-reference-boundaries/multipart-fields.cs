using System.Net.Http;
class FormSender {
    async void Send(string endpoint) {
        var client = new HttpClient();
        var content = new MultipartFormDataContent();
        content.Add(new StringContent("example"), "message");
        await client.PostAsync(endpoint, content);
    }
}
