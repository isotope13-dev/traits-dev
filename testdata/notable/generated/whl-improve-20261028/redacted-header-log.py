def record(request, client):
    headers = dict(request.headers)
    safe = redact(headers)
    client.send_log({"headers": safe})
