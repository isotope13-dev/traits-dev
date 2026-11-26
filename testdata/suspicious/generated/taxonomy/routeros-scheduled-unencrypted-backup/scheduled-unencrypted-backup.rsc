/system script add name=mv-backup policy=read,write,test,sensitive source="/system backup save name=mv-backup dont-encrypt=yes"
/system scheduler add name=mv-backup interval=1d start-time=03:00:00 policy=read,write,test,sensitive on-event="/system script run mv-backup"
