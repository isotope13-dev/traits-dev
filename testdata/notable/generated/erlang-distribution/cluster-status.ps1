# Get-Content 'C:\RabbitMQ\.erlang.cookie'
# rpc:call('rabbit@peer',os,cmd,[[104,111,115,116]])
Write-Output 'documentation only'
$data = Get-Content 'C:\RabbitMQ\settings.config'
$path = 'C:\RabbitMQ\.erlang.cookie'
& 'C:\RabbitMQ\erl.exe' -noshell -sname monitor -setcookie $secret -eval "rpc:call('rabbit@peer',rabbit,status,[]),halt()."
