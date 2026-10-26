// Harmless documentation constants: no main, file writes, or service calls.
// Rebuild: javac -g:none -d testdata/benign testdata/benign/LaunchdConstants.java
final class LaunchdConstants {
    static final String DIRECTORY = "/Library/LaunchDaemons";
    static final String EXAMPLE =
        "<plist><dict><key>KeepAlive</key><true/>" +
        "<key>ProgramArguments</key><array><string>/usr/bin/true</string>" +
        "</array></dict></plist>";
}
