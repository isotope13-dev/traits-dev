#!/bin/sh
/opt/zimbra/bin/zmlocalconfig -s -m nokey ldap_master_url
/opt/zimbra/common/bin/ldapsearch -x -H ldap://localhost -b cn=zimbra '(objectClass=*)' zimbraServiceHostname
/opt/zimbra/bin/zmprov gd example.invalid zimbraMailHost
