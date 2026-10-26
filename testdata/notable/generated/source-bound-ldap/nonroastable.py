import socket
from impacket.ldap import ldap, ldapasn1

original_connect = socket.socket.connect

def routed_connect(self, destination):
    self.bind(("192.0.2.10", 0))
    return original_connect(self, destination)

socket.socket.connect = routed_connect

connection = ldap.LDAPConnection("ldap://dc.example.invalid", "dc=example,dc=invalid")
connection.login("audit", "placeholder", "EXAMPLE")

filters = [
    "(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=512))",
    "(&(objectClass=user)(mail=*)(!(objectClass=computer))(!(cn=krbtgt)))",
]
for query in filters:
    results = connection.search(searchFilter=query,
                                attributes=["sAMAccountName", "servicePrincipalName", "adminCount"])
    for entry in results:
        if isinstance(entry, ldapasn1.SearchResultEntry):
            print(entry)
