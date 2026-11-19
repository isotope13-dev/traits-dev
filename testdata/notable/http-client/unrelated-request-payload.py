import http.client
probe = "/?id=1%27%20OR%20%271%27%3D%271"
class Queue:
    def request(self, verb, path): pass
unused = http.client.HTTPConnection("example.test")
q = Queue()
q.request("GET", probe)
