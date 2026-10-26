$x.GetMethods() | Where-Object { $_.Name -like "*FromBase64*" }
