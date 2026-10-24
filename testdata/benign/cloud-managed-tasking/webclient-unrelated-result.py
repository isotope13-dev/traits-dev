from System.Net import WebClient

def report(method, url):
    client = WebClient()
    result = method.GetMethod("Report").Invoke(None, None)
    client.UploadString(url, "PUT", "fixed report")
