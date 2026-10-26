This example builds an authenticated HTTP request and inspects it locally.

```go
token := os.Getenv("SERVICE_TOKEN")
headers["Authorization"] = "Bearer " + token
dump, err := httputil.DumpRequest(req, true)
```
