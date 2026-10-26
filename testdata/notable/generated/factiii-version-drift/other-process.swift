import Foundation
let p = Process()
p.executableURL = URL(fileURLWithPath: "/usr/bin/other")
p.arguments = ["load"]
try p.run()
