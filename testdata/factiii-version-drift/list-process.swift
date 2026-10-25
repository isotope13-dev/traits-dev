import Foundation
let p = Process()
p.executableURL = URL(fileURLWithPath: "/bin/launchctl")
p.arguments = ["list"]
try p.run()
