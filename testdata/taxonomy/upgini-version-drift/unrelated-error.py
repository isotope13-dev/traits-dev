def report(response):
    err = response.json()["errors"][0]
    track = {"visitorId": "anonymous"}
    return err, track
