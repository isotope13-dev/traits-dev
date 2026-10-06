import urllib.request

def load(url):
    source = urllib.request.urlopen(url).read()
    exec(compile(source, "<profile>", "exec"), {})
