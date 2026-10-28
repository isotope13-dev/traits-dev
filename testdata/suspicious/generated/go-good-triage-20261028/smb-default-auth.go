package client
func login() { s, _ := smb.NewSession(host, false); s.Authenticate("administrator", "password") }
