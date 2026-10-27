from System.Net import WebClient

class LocalCatalog:
    def DownloadString(self, key):
        return key

client = LocalCatalog()
print(client.DownloadString("https://example.org/catalog-key"))
