function removeLogs(nativeBridge) {
    nativeBridge.deleteFileAtPath('/var/mobile/Library/Logs/CrashReporter/ExcUserFault_com.apple.WebKit.WebContent.ips');
}
