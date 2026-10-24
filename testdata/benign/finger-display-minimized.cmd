start "" /min cmd.exe /c for /f "delims=" %%q in ('finger.exe admin@directory.example') do echo %%q
