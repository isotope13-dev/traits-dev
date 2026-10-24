import AVFoundation
import WebKit
import JavaScriptCore
import CryptoKit
import Security
import zlib

func exerciseAPIs(_ url: URL) throws {
    let context = JSContext()!
    context.evaluateScript("1 + 2")
    let view = WKWebView()
    view.evaluateJavaScript("document.title", completionHandler: nil)
    AVAudioSession.sharedInstance().requestRecordPermission { _ in }
    let recorder = try AVAudioRecorder(url: url, settings: [:])
    let digest256 = SHA256.hash(data: Data())
    let digest512 = SHA512.hash(data: Data())
    var stream = z_stream()
    inflate(&stream, Z_NO_FLUSH)
    var bytes = [UInt8](repeating: 0, count: 32)
    SecRandomCopyBytes(kSecRandomDefault, bytes.count, &bytes)
}
