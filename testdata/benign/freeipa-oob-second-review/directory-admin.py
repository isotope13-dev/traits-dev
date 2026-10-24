# An authenticated operator clears management metadata on an OTP entry.
from ldap3 import Connection
conn = Connection('directory.example', user='operator', password='operator-key')
conn.bind()
attributes = {'ipaTokenOwner': '', 'managedBy': ''}
conn.modify('ipaTokenUniqueID=token,cn=otp,dc=example,dc=org', attributes)
