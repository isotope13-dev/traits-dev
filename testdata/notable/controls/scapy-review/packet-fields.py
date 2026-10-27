from scapy.all import ICMPv6EchoRequest
packet = ICMPv6EchoRequest(code=0xff, data="test data")
