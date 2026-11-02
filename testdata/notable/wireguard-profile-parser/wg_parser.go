package wgparse

func parseKey(key, value string, cfg *Config) {
	switch key {
	case "PrivateKey":
		cfg.PrivateKey = value
	case "ListenPort":
		cfg.ListenPort = value
	case "AllowedIPs":
		cfg.AllowedIPs = value
	}
}
