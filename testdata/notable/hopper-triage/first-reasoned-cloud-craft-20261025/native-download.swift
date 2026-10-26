import Foundation
let session = URLSession.shared
let request = URLRequest(url: URL(string: "https://example.com/movie.mp4")!)
let transfer = session.downloadTask(with: request)
transfer.resume()
