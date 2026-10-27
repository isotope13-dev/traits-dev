% Packet regression campaign
+ Packet construction
= Echo payload field
a = ICMPv6EchoRequest(data="test data")
= Packet exchange
sr1(IP(dst="127.0.0.1")/ICMP(), timeout=1)
= Local pipe
r,w = os.pipe()
= Legacy decoder
text = """
YWJj""".decode("base64")
= Construct padding
buffer = "A"*4000
= Function calls
ls()
lsc()
a = IPv3()
while True:
    break

= ARP probe
arping(_+"/24")
