def prepare_review(original):
    request = dict(original)
    request["metadata"] = dict(original["metadata"])
    request["ping_recipients"] = []
    request["page_recipients"] = []
    request["metadata"]["no_notify"] = True
    request["metadata"]["notification_suppression"] = {
        "reason": "User explicitly requested no messages",
        "original_ping_recipients": original.get("ping_recipients", []),
        "original_page_recipients": original.get("page_recipients", []),
    }
    return request


def persist_review(row, publish):
    if row["no_notify"] is not True:
        raise ValueError("This task must not send notifications")
    return publish(row)
