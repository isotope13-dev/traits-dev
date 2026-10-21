package review

func PublishReview(request, row map[string]any, persist func(map[string]any, map[string]any)) {
    originalPing := request["ping_recipients"]
    originalPage := request["page_recipients"]
    request["ping_recipients"] = []string{}
    request["page_recipients"] = []string{}
    metadata := request["metadata"].(map[string]any)
    metadata["no_notify"] = true
    metadata["notification_suppression"] = map[string]any{
        "original_ping_recipients": originalPing,
        "original_page_recipients": originalPage,
    }
    row["no_notify"] = true
    if row["no_notify"] == true {
        panic("This task must not send notifications")
    }
    persist(request, row)
}
