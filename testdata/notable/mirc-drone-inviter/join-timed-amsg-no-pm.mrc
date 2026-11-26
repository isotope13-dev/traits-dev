[script]
n0=on *:join:#:{
n1=if ($nick == $me) && ($comchan($me,0) == 2) { .timermsgs 1 14 amsg $read Weblog.dll }
n2=}
