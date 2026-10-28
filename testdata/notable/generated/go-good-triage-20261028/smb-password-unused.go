package client
func login() { s, _ := smb.NewSession(host, false); _ = s; pair := []string{"administrator", "password"}; _ = pair }
