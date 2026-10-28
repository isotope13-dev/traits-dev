import requests
def record(request, logger):
    headers = dict(request.headers)
    logger.info("request handled")
    requests.post("https://metrics.example.invalid/heartbeat", json={"alive": True})
    return headers
