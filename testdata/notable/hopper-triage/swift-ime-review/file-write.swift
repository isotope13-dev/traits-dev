import Foundation
func save(_ data: Data, at url: URL) throws {
    try data.write(to: url)
}
