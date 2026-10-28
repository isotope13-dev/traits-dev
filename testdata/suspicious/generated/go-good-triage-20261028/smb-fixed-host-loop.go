package client

func login(host string, rows []string) {
	for _, row := range rows {
		s, _ := smb.NewSession(host, false)
		s.Authenticate("administrator", "password")
		println(row)
	}
}
