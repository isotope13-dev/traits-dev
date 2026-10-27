do shell script "curl -X POST -H \"buildid: example\" --data-binary @/tmp/report.zip https://example.invalid/upload"
do shell script "rm -r " & stagingDirectory
