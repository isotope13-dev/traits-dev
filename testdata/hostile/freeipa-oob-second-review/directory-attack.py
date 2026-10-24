from ldap3 import Connection, ANONYMOUS, MODIFY_ADD
directory_client = Connection('directory.example', authentication=ANONYMOUS)
directory_client.bind()
attributes = {
    'objectClass': ['ipaTokenTOTP', 'krbPrincipalAux'],
    'ipaTokenOwner': '', 'managedBy': '',
    'krbPrincipalName': 'operator@EXAMPLE.ORG',
    'krbPrincipalKey': b'provided-kerberos-key', 'userPassword': 'provided-password'
}
directory_client.add('ipaTokenUniqueID=token,cn=otp,dc=example,dc=org', attributes=attributes)
changes = {'member': [(MODIFY_ADD, ['krbPrincipalName=operator@EXAMPLE.ORG,cn=otp,dc=example,dc=org'])]}
directory_client.modify('cn=admins,cn=groups,cn=accounts,dc=example,dc=org', changes)
