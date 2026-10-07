import Foundation

// Dropper control: base64 payload decoded and piped into a shell in one
// flow. The file-scoped loader must fire here.
let blob = "ZWNobyBoZWxsbw=="
let task = Process()
task.executableURL = URL(fileURLWithPath: "/bin/sh")
task.arguments = ["-c", String(data: Data(base64Encoded: blob)!, encoding: .utf8)!]
try task.run()
