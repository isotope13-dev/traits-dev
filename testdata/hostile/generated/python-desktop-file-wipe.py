import os

desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
for name in os.listdir(desktop):
    os.remove(os.path.join(desktop, name))
