/system script add name=mv-notable policy=read,write,test source="/system backup save name=mv-notable"
/system scheduler add name=mv-notable interval=1d start-time=03:00:00 on-event="/system script run mv-notable"
