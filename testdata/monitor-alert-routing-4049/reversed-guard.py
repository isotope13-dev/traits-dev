from copy import deepcopy


def publish_review(request, row, persist):
    original = deepcopy(request)
    request = deepcopy(request)
    request["ping_recipients"] = []
    request["page_recipients"] = []
    request["metadata"]["no_notify"] = True
    request["metadata"]["notification_suppression"] = {
        "reason": "User explicitly requested no messages",
        "original_ping_recipients": original.get("ping_recipients", []),
        "original_page_recipients": original.get("page_recipients", []),
    }
    row = dict(row)
    row["no_notify"] = True
    if row["no_notify"] is True:
        raise ValueError("This task must not send notifications")
    return persist(request, row)
