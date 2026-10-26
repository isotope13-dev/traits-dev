@echo off
finger admin@directory.example
for /f "delims=" %%q in ('finger admin@directory.example') do echo %%q
