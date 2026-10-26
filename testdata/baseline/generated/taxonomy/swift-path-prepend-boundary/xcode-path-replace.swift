import Foundation

// Xcode build-phase helper: preserve the caller's PATH so tools installed
// outside the launchd environment (e.g. a Homebrew prefix) stay visible.
func ninjaBuildScript(path: String) -> String {
    var script = ""
    script += """
      export PATH="\(path)"

      """
    script += "ninja -C build -- all\n"
    return script
}
