def record(request, client):
    details = {"headers": dict(request.headers)}
    details = {"status": "ok"}
    client.send_log(details)
