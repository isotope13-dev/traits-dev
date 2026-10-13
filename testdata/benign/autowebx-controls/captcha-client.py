from requests import post

def solve(client_key, site, key):
    task = {"clientKey": client_key, "task": {
        "type": "RecaptchaV2TaskProxyless",
        "websiteURL": site, "websiteKey": key}}
    response = post("https://api.solver.example/createTask", json=task).json()
    return post("https://api.solver.example/getTaskResult",
                json={"clientKey": client_key, "taskId": response["taskId"]}).json()
