from impacket.smbconnection import ApplicationClient
smb = ApplicationClient(target, target)
smb.login(user, "", domain, lm_hash, nt_hash)
