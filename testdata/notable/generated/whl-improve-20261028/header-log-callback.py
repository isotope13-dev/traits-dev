def attach(app, request, client):
    @app.after_request
    def after_request(response):
        details = {"headers": dict(request.headers)}
        client.send_log(details)
        return response
