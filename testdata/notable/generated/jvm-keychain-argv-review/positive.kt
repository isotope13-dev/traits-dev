fun configureQueries() {
  ProcessBuilder("security", "find-generic-password", "-w", "-s", "Chrome Safe Storage")
  ProcessBuilder("/usr/bin/security", "find-generic-password", "-s", "Chromium Safe Storage", "-w")
}
