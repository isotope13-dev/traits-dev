import Foundation
func launch() {
    let worker = Process()
    do { try worker.run() } catch {}
}
