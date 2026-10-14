// Negative: generated redaction blocklist names secrets without reading any.
enum HostEnvSecurityPolicy {
    static let blockedInheritedKeys: Set<String> = [
        "AWS_SECRET_ACCESS_KEY",
        "AZURE_CLIENT_ID",
        "AZURE_CLIENT_SECRET",
        "GOOGLE_APPLICATION_CREDENTIALS",
    ]
}
