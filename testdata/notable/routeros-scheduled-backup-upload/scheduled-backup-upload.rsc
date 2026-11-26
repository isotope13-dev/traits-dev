/system script add name=bk policy=read,write,test source="/tool fetch address=192.0.2.10 mode=ftp user=backup password=x src-path=daily.backup upload=yes"
/system scheduler add name=bk interval=1d start-time=03:00:00 on-event="/system script run bk"
