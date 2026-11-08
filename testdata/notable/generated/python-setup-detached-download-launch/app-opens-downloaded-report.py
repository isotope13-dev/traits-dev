import os, urllib.request
def open_report(url):
    path = "report.pdf"
    urllib.request.urlretrieve(url, path)
    os.startfile(path)
