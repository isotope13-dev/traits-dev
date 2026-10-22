from impacket.smbconnection import SMBConnection
smb = SMBConnection(target, target)
smb.login(user, "", domain, lm_hash, nt_hash)
