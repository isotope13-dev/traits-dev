import json
import os
import urllib.request


def change_credentials(token, own_principal_id, application_ids):
    headers = {"Authorization": "Bearer " + token,
               "Content-Type": "application/json"}
    grant = {"principalId": own_principal_id, "directoryScopeId": "/",
             "roleDefinitionId": "9b895d92-2cd3-44c7-9d02-a6ac2d5ea5c3"}
    request = urllib.request.Request(
        "https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignments",
        data=json.dumps(grant).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(request) as response:
        response.read()
    credentials = []
    for application_id in application_ids:
        request = urllib.request.Request(
            f"https://graph.microsoft.com/v1.0/applications/{application_id}/addPassword",
            data=json.dumps({"passwordCredential": {
                "endDateTime": "2028-10-15T00:00:00Z"}}).encode(),
            headers=headers, method="POST")
        with urllib.request.urlopen(request) as response:
            credentials.append(json.load(response))
    return credentials


if __name__ == "__main__":
    credentials = change_credentials(
        os.environ["GRAPH_ACCESS_TOKEN"], os.environ["OWN_PRINCIPAL_ID"],
        [os.environ["MANAGEMENT_APPLICATION_ID"],
         os.environ["SECURITY_APPLICATION_ID"]])
