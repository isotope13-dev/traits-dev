-- Static control: report upload without credential targets or persistence.
do shell script "ditto -c -k --sequesterRsrc /tmp/report /tmp/report.zip"
do shell script "curl -X POST -F \"file=@/tmp/report.zip\" https://example.invalid/reports"
