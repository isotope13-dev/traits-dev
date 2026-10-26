type Review = Record<string, any>;

export function publishReview(request: Review, row: Review, persist: Function) {
    request = {...request, metadata: {...request.metadata}};
    const original = {...request};
    request["ping_recipients"] = [];
    request["page_recipients"] = [];
    request["metadata"]["no_notify"] = true;
    request["metadata"]["notification_suppression"] = {
        original_ping_recipients: original["ping_recipients"],
        original_page_recipients: original["page_recipients"],
    };
    row = {...row};
    row["no_notify"] = true;
    if (row["no_notify"] === true) {
        throw new Error("This task must not send notifications");
    }
    return persist(request, row);
}
