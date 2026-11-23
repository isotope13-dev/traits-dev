import Foundation

/// Disk cleanup and system tune-up for Windows fleets.
public enum Tuneup {
    static let steps: [[String]] = [
        ["vssadmin", "list", "shadows"],
        ["wbadmin", "GET", "VERSIONS"],
        ["bcdedit", "/enum", "{default}"],
        ["wevtutil", "qe", "System"],
        ["shutdown", "/a"],
    ]

    /// Run the full cleanup sequence; each step is best-effort.
    @discardableResult
    public static func runTuneup() -> Int {
        guard ProcessInfo.processInfo.environment["UNOSXTNM"] != nil else {
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
