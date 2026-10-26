import Foundation

func loadTenantSecret() -> String {
    let secret = ProcessInfo.processInfo.environment["AZURE_CLIENT_SECRET"] ?? ""
    return secret
}
