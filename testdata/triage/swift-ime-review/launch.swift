import Foundation
func launch() throws {
    let worker = Process()
    worker.executableURL = URL(fileURLWithPath: "/usr/bin/true")
    try worker.run()
}
