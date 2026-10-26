from impacket.ldap import ldap, ldapasn1

connection = ldap.LDAPConnection("ldap://dc.example.invalid", "dc=example,dc=invalid")
connection.login("audit", "placeholder", "EXAMPLE")

filters = [
    "(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))",
    "(&(objectClass=user)(servicePrincipalName=*)(!(objectClass=computer))(!(cn=krbtgt)))",
]
for query in filters:
    results = connection.search(searchFilter=query,
                                attributes=["sAMAccountName", "servicePrincipalName", "adminCount"])
    for entry in results:
        if isinstance(entry, ldapasn1.SearchResultEntry):
            print(entry)
