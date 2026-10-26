on *:TEXT:!status:*:{ echo -a $gettok(%line,1,32) }
on *:SOCKREAD:test:{ sockread %line }
alias connect-test { sockopen test localhost 1234 }
alias auth { sockwrite $sockname PWD $+ 14438136782715101980 }
