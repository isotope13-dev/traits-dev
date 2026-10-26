<?php
function publish_review(array $request, array $row, callable $persist) {
    $original = $request;
    $request["metadata"]["no_notify"] = true;
    $request["metadata"]["notification_suppression"] = [
        "original_ping_recipients" => $original["ping_recipients"],
        "original_page_recipients" => $original["page_recipients"],
    ];
    $row["no_notify"] = true;
    if ($row["no_notify"] !== true) {
        throw new RuntimeException("This task must not send notifications");
    }
    return $persist($request, $row);
}
