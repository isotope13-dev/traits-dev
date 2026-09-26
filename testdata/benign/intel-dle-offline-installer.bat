@echo on
REM Description: Install Intel Support Packages on Windows CI runners
set XPU_BUNDLE_URL=https://registrationcenter-download.intel.com/akdlm/IRC_NAS/d2148e15-b3c4-4313-afa9-a2373318b0b5/intel-deep-learning-essentials-2026.0.0.613_offline.exe
:xpu_bundle_install
curl -o xpu_bundle.exe --retry 3 --retry-all-errors -k %XPU_BUNDLE_URL%
echo "XPU Bundle installing..."
start /wait "Intel Bundle Installer" "xpu_bundle.exe" --action=install --eula=accept --silent
if errorlevel 1 exit /b 1
del xpu_bundle.exe
