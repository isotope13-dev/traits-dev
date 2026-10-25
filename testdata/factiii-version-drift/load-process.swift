import Foundation
let p = Process()
p.executableURL = URL(fileURLWithPath: "/bin/launchctl")
p.arguments = ["load", "-w", path]
try p.run()
