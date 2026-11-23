object Maintenance {
    fun install() {
        ProcessBuilder("schtasks", "/Create", "/TN", "LocalCleanup",
            "/SC", "MINUTE", "/MO", "60", "/TR",
            "powershell -NoProfile -w hidden -File C:\\Tools\\Cleanup.ps1", "/F").start()
    }
}
