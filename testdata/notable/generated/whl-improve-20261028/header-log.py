def record(request, client):
    record = {"headers": dict(request.headers)}
    client.send_log(record)
