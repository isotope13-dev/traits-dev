$x.GetMethods() | Where-Object { $_.Name -like "*ToBase64*" }
