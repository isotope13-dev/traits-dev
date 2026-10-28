param([string]$Url, [string]$Destination)
try {
    Invoke-WebRequest -Uri $Url -OutFile $Destination -UseBasicParsing
} catch {
    & curl.exe -L -o $Destination $Url
}
