import AppKit
import Foundation

enum DebugActions {
    @MainActor
    static func restartApp() {
        let url = Bundle.main.bundleURL
        let task = Process()
        // Relaunch shortly after this instance exits.
        task.launchPath = "/bin/sh"
        task.arguments = ["-c", "sleep 0.2; open -n \"$1\"", "_", url.path]
        try? task.run()
        NSApp.terminate(nil)
    }

    static func killProcess(_ pid: Int) async -> Bool {
        let primary = await ShellExecutor.run(command: ["kill", "-TERM", "\(pid)"], cwd: nil, env: nil, timeout: 2)
        return primary.ok
    }
}
