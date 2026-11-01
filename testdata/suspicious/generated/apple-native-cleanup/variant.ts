function removeLogs(nativeBridge: {deleteFileAtPath(path: string): void}) {
    nativeBridge.deleteFileAtPath('/var/mobile/Library/Logs/CrashReporter/JetsamEvent.ips');
}
