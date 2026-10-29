package logging

func warning(message string) {
	log.Print("check_id: disk-space")
	log.Print("[WARN]: " + message)
}
