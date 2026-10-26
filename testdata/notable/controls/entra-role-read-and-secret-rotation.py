import json
import urllib.request

headers = {"Authorization": "Bearer supplied-token", "Content-Type": "application/json"}
# Inspect an existing Global Administrator assignment, then rotate an app secret.
# A POST elsewhere in this file must not promote this GET to a role grant.
query = urllib.request.Request(
    "https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignments?$filter=roleDefinitionId eq '62e90394-69f5-4237-9190-012177145e10'",
    headers=headers, method="GET")
with urllib.request.urlopen(query) as response:
    print(response.read())
rotate = urllib.request.Request(
    "https://graph.microsoft.com/v1.0/applications/00000000-0000-0000-0000-000000000001/addPassword",
    data=json.dumps({"passwordCredential": {"displayName": "scheduled-rotation"}}).encode(),
    headers=headers, method="POST")
with urllib.request.urlopen(rotate) as response:
    print(response.read())
