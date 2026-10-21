def publish_review(request, row, persist)
  original = request.dup
  request = request.dup
  request["metadata"] = request["metadata"].dup
  request["ping_recipients"] = []
  request["page_recipients"] = []
  request["metadata"]["no_notify"] = true
  request["metadata"]["notification_suppression"] = {
    "original_ping_recipients" => original["ping_recipients"],
    "original_page_recipients" => original["page_recipients"]
  }
  row = row.dup
  row["no_notify"] = true
  if row["no_notify"] == true
    raise "This task must not send notifications"
  end
  persist.call(request, row)
end
