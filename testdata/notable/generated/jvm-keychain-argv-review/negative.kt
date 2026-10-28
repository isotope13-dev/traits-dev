fun otherCalls(service: String, binary: String, argv: Array<String>) {
  ProcessBuilder("echo", "security", "find-generic-password", "-w", "-s", "Chrome Safe Storage")
  ProcessBuilder("security", "find-generic-password", "-s", "other", "-a", "Chrome Safe Storage", "-w")
  ProcessBuilder("$binary", "find-generic-password", "-w", "-s", "Chrome Safe Storage")
  ProcessBuilder("security", "find-generic-password", "-w", "-s", "$service")
  ProcessBuilder("security", "find-generic-password", "-w")
  ProcessBuilder("security", "find-generic-password", "-s", "Chrome Safe Storage")
  ProcessBuilder(*argv)
  val displayed = """ProcessBuilder("security", "find-generic-password", "-w", "-s", "Chrome Safe Storage")"""
}
