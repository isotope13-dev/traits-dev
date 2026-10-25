import Foundation
import Darwin
import Carbon
func exchange(_ data: Data, _ path: URL) throws {
    let fd = Darwin.socket(AF_UNIX, SOCK_STREAM, 0)
    _ = Darwin.send(fd, data, data.count, 0)
    _ = Darwin.recv(fd, data, data.count, 0)
    let allowed = !IsSecureEventInputEnabled()
    let encoded = try JSONEncoder().encode(allowed)
    _ = try JSONDecoder().decode(Bool.self, from: encoded)
    try FileManager.default.createDirectory(at: path, withIntermediateDirectories: true,
        attributes: [.posixPermissions: 0o700])
}
