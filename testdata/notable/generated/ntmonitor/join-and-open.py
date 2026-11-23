import os
filename = "settings.dat"
path = os.path.join("/srv/app", filename)
handle = open(path)
