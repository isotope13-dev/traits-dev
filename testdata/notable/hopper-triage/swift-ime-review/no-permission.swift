import Foundation
import Darwin
func prepare(_ path: URL) throws {
    let fd = Darwin.socket(AF_INET, SOCK_STREAM, 0)
    try FileManager.default.createDirectory(at: path, withIntermediateDirectories: true)
}
