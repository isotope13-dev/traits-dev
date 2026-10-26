from mitmproxy import http
def request(flow):
    if flow.request.path.endswith("/git-receive-pack"):
        flow.request.path = flow.request.path + "?service=git-upload-pack"
