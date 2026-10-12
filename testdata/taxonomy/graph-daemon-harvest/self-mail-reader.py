"""Benign control: personal Graph mail reader using delegated access to the
caller's own mailbox only. No daemon credentials, no cross-user access, no
date-windowed bulk pull, no local staging or upload."""

import requests

GRAPH_ROOT = "https://graph.microsoft.com/v1.0/me/messages"


def read_own_mail(session, top=10):
    response = session.get(GRAPH_ROOT, params={"$top": top})
    return response.json().get("value", [])


def main(token):
    session = requests.Session()
    session.headers["Authorization"] = "Bearer " + token
    for message in read_own_mail(session):
        print(message.get("subject"))
