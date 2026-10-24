import Foundation
struct Example {
    func evaluateScript(_ text: String) {}
    func evaluateJavaScript(_ text: String) {}
}
let example = Example()
example.evaluateScript("plain text")
example.evaluateJavaScript("plain text")
