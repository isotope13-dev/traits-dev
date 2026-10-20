import urllib.request
token = open("/var/run/secrets/kubernetes.io/serviceaccount/token").read()
request = urllib.request.Request("https://kubernetes.default.svc/api/v1/pods", headers={"Authorization": "Bearer " + token})
urllib.request.urlopen(request)
