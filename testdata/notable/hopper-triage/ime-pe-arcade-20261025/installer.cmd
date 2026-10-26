@echo off
powershell -NoProfile -ExecutionPolicy Bypass -Command "irm 'https://downloads.example.invalid/install.ps1' | iex"
