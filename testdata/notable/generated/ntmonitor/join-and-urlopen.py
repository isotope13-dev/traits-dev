import os
from urllib.request import urlopen
filename = "settings.dat"
path = os.path.join("/srv/app", filename)
response = urlopen(path)
