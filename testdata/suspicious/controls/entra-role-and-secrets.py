import json
import os
import urllib.request

headers = {"Authorization": "Bearer " + os.environ["GRAPH_TOKEN"], "Content-Type": "application/json"}
request = urllib.request.Request(
    "https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignments",
    data=json.dumps({
        "roleDefinitionId": "62e90394-69f5-4237-9190-012177145e10",
        "principalId": os.environ["ACTOR_PRINCIPAL_ID"],
        "directoryScopeId": "/"
    }).encode(), headers=headers, method="POST")
with urllib.request.urlopen(request) as response:
    response.read()
for application in os.environ["TARGET_APPLICATION_IDS"].split(","):
    request = urllib.request.Request(
        f"https://graph.microsoft.com/v1.0/applications/{application}/addPassword",
        data=json.dumps({"passwordCredential": {"displayName": "service-access", "endDateTime": "2028-10-15T00:00:00Z"}}).encode(),
        headers=headers, method="POST")
    with urllib.request.urlopen(request) as response:
        print(json.load(response)["secretText"])
