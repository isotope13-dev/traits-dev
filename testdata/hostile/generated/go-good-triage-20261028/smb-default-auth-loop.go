package client
func spray(hosts []string) { for _, host := range hosts { s, _ := smb.NewSession(host, false); s.Authenticate("administrator", "password") } }
