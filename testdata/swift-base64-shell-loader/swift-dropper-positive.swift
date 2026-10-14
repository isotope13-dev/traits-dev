import Foundation
if let data = Data(base64Encoded: "ZWNobyBoZWxsbwo="),
   let cmd = String(data: data, encoding: .utf8) {
    let task = Process()
    task.launchPath = "/bin/sh"
    task.arguments = ["-c", cmd]
    try? task.run()
    task.waitUntilExit()
}
