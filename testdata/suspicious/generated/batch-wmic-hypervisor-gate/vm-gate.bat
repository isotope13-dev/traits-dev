@echo off
rem hypervisor gate before running the payload
for /f "tokens=*" %%a in ('wmic computersystem get manufacturer ^| findstr /i "VMware\|Virtual\|QEMU\|VBOX"') do (
    exit /b
)
echo ready
