# Nightly documents backup control: zips the Documents tree and uploads the
# single archive to the company backup endpoint. No private-key material is
# targeted and no webhook message body is posted, so this must never read
# as credential theft or webhook exfiltration.
$stamp = Get-Date -Format 'yyyyMMdd'
$archive = "$env:TEMP\docs-backup-$stamp.zip"

Get-ChildItem -Path "$env:USERPROFILE\Documents" -Include "*.docx","*.xlsx","*.pdf","*.txt" -Recurse |
    Compress-Archive -DestinationPath $archive -Force

Invoke-RestMethod -Uri 'https://backup.internal.example.com/upload' -Method Post -InFile $archive -ContentType 'application/zip'
