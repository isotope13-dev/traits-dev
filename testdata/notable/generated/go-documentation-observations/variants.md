These alternate APIs check whether the variable exists and dump a client request.

```go
token, present := os.LookupEnv ("SERVICE_TOKEN")
headers [ "Authorization" ] = "Bearer " + token
dump, err := httputil.DumpRequestOut (req, false)
```
