import requests

def add_administrator(crowd, auth, username):
    return requests.post(crowd + '/rest/usermanagement/1/group/user/direct?groupname=jira-administrators', auth=auth, json={'name': username})
