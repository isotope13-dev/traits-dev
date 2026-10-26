import Foundation
let session = URLSession.shared
let file = URL(fileURLWithPath: "/tmp/export.csv")
let request = URLRequest(url: URL(string: "https://example.com/submit")!)
let transfer = session.uploadTask(with: request, fromFile: file)
transfer.resume()
