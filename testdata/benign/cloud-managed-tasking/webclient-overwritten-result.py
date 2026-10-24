from System.Net import WebClient

def report(method, url):
    client = WebClient()
    result = method.GetMethod("Report").Invoke(None, None)
    result = "fixed report"
    client.UploadString(url, "PUT", str(result))
