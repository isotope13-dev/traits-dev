import os
def install():
    folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    if folder:
        path = os.path.join(folder, 'welcome.pyw')
        open(path, 'w').write('print("welcome")')
