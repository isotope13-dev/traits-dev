import Network
import Foundation
let watcher = NWPathMonitor()
watcher.start(queue: DispatchQueue(label: "connectivity"))
