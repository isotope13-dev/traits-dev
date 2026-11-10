import shutil, zipfile
from urllib.request import urlretrieve
def update():
    archive = urlretrieve("https://example.com/a.zip")[0]
    shutil.rmtree("appdir")
    with zipfile.ZipFile(archive) as f:
        for info in f.infolist():
            f.extract(info, "appdir")
