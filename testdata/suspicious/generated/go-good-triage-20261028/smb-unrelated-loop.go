package client

func login(host string, rows []string) {
	s, _ := smb.NewSession(host, false)
	s.Authenticate("administrator", "password")
	for _, row := range rows {
		println(row)
	}
}
