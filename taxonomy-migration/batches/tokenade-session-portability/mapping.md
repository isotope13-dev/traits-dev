# Tokenade trait dispositions

Unlisted source IDs retain their original matcher and placement. Effective defaults are preserved. Intentional coverage changes are discussed in README.md.

```text
objectives/credential-access/browser/chromium::master-decrypt -> micro-behaviors/data/config/browser-preference::chromium-encrypted-key-metadata
objectives/credential-access/browser/chromium::powershell-cookie-sql -> micro-behaviors/data/db/read/records::powershell-cookie-table-select
objectives/credential-access/browser/safari::cookie-theft -> micro-behaviors/communications/http/cookie-store::chromium-cookie-query-with-browser-path
micro-behaviors/communications/http/cookie-store::browser-cookie-store-query -> micro-behaviors/communications/http/cookie-store::browser-cookie-store-query
objectives/credential-access/browser/devtools::chromium-cdp-discovered-cookie-harvest -> micro-behaviors/communications/http/devtools/client::cdp-discovered-cookie-jar-read
objectives/anti-static/obfuscation/encoding/ip-notation::ipv4-struct-pack -> micro-behaviors/data/serialize/binary::python-pack-hex-u32
objectives/collection/clipboard/monitor::message-loop-str -> micro-behaviors/os/message/queue::message-loop-string
objectives/command-and-control/backdoor/webshell/deny::drf-forbidden-status -> micro-behaviors/communications/http/response::python-forbidden-status-argument
objectives/command-and-control/backdoor/webshell/deny::drf-authorization-response-marker -> micro-behaviors/communications/http/response::drf-authorization-response
objectives/command-and-control/channel/http-beacon::chrome-spoof-user-agent-script -> micro-behaviors/communications/http/user-agent::chrome-user-agent-script
objectives/credential-access/browser/chromium::amazon-cookie-domain -> micro-behaviors/communications/url/host/domain-http::amazon-commerce-domain
objectives/credential-access/browser/chromium::browser-creds-table-sql -> micro-behaviors/data/db/read/records::browser-record-table-select
objectives/credential-access/browser/chromium::chrome-safe-storage-keychain-query -> micro-behaviors/os/security/keychain::chrome-safe-storage-query
objectives/credential-access/browser/chromium::python-dpapi-browser-decrypt -> micro-behaviors/os/security/dpapi::python-chromium-key-unprotect
objectives/credential-access/browser/firefox::local-storage-access -> micro-behaviors/fs/path/application/browser/storage::firefox-storage-database-reference
objectives/credential-access/browser/account-page::auth-storage-read-call -> micro-behaviors/data/db/read/key-value::auth-token-getitem-source
objectives/credential-access/browser/session-hijack::jwt-file-or-browser-read--rx-1 -> micro-behaviors/fs/path/cookie::firefox-cookies-sqlite-filename
micro-behaviors/os/security/keychain::python-find-generic-password -> micro-behaviors/os/security/keychain::python-find-generic-password
micro-behaviors/data/collection/wordlist::python-password-list-loop -> micro-behaviors/data/collection/wordlist::python-password-list-loop
micro-behaviors/data/db/write::last-checked-sql-assignment -> micro-behaviors/data/db/write::last-checked-sql-assignment
objectives/evasion/decoy/cloaking::js-fake-cloudflare -> micro-behaviors/ui/controls/credential::human-verification-marker
objectives/evasion/decoy/lure::browser-verification-interstitial -> micro-behaviors/ui/controls/credential::browser-verification-status-text
objectives/supply-chain/hidden-payload/native-extension::python-release-manifest-reference -> micro-behaviors/fs/path/metadata-store::python-manifest-json-filename
metadata/package/documentation/claims::browser-session-extraction-description -> metadata/package/documentation/claims::browser-session-extraction-description
metadata/package/documentation/claims::portable-browser-session-description -> metadata/package/documentation/claims::portable-browser-session-description
metadata/package/documentation/claims::donor-session-replay-description -> metadata/package/documentation/claims::donor-session-replay-description
metadata/package/documentation/claims::package-advertises-browser-session-replay -> metadata/package/documentation/claims::package-advertises-browser-session-replay
micro-behaviors/communications/http/cookie-name::apisid-sapisid-cookie-pair -> micro-behaviors/communications/http/cookie-name::apisid-sapisid-cookie-pair
micro-behaviors/communications/http/cookie-name::entra-session-cookie-name -> micro-behaviors/communications/http/cookie-name::entra-session-cookie-name
micro-behaviors/communications/http/cookie-name::microsoft-signin-state-cookie-name -> micro-behaviors/communications/http/cookie-name::microsoft-signin-state-cookie-name
micro-behaviors/communications/http/cookie-name::idp-session-cookie-named -> micro-behaviors/communications/http/cookie-name::idp-session-cookie-named
objectives/credential-access/browser/session-hijack::idp-session-cookie-targeting -> micro-behaviors/communications/http/cookie-name::idp-session-cookie-targeting
objectives/credential-access/theft/file::android-browser-secret-path -> micro-behaviors/fs/path/application/browser/storage::android-chromium-secret-store-path
objectives/credential-access/theft/keywords::token -> micro-behaviors/data/parse/vocabulary::token-extraction-wording
objectives/credential-access/phishing/landing::headlesschrome-match -> micro-behaviors/os/sysinfo/platform/browser::headlesschrome-string-test
objectives/anti-analysis/sandbox-detect/tool-references::js-phantom-nightmare-globals--rx-3 -> micro-behaviors/os/sysinfo/platform/browser::nightmare-automation-global-reference
objectives/anti-analysis/sandbox-detect/tool-references::js-phantom-nightmare-globals--rx-4 -> micro-behaviors/os/sysinfo/platform/browser::chrome-automation-global-reference
objectives/credential-access/wallet/mnemonic::phantom-word-unless-cond-1--rx-2 -> micro-behaviors/os/sysinfo/platform/browser::callphantom-global-reference
objectives/discovery/host/browser/identity::browser-names -> micro-behaviors/os/application/target/browser::multiple-browser-names
objectives/discovery/host/browser/identity::chromium-binary-basename -> metadata/filename/name-form::chromium-basename-word
objectives/discovery/host/browser/identity::safari-binary-basename -> metadata/filename/name-form::safari-basename-word
objectives/discovery/host/browser/identity::safari-plist -> micro-behaviors/fs/path/config/app::safari-preferences-plist
micro-behaviors/fs/path/personal::safari-history-db -> micro-behaviors/fs/path/personal::safari-history-db
objectives/discovery/host/browser/identity::safari-history -> micro-behaviors/fs/path/application/browser/profile::safari-data-path-reference
micro-behaviors/fs/path/application/browser/profile::chromium-profile-subdirectory-reference -> micro-behaviors/fs/path/application/browser/profile::chromium-profile-subdirectory-reference
objectives/discovery/host/browser/identity::multi-browser-enum -> micro-behaviors/fs/path/application/browser/profile::multiple-browser-data-references
micro-behaviors/communications/proxy/turn::webrtc-empty-ice-servers -> micro-behaviors/communications/proxy/turn::webrtc-empty-ice-servers
micro-behaviors/communications/proxy/turn::local-ip-list-symbol -> micro-behaviors/communications/proxy/turn::local-ip-list-symbol
micro-behaviors/communications/proxy/turn::webrtc-local-ip-discovery -> micro-behaviors/communications/proxy/turn::webrtc-local-ip-discovery
micro-behaviors/communications/http/header/accept::script-client-browser-header-pair -> micro-behaviors/communications/http/header/accept::script-client-browser-header-pair
metadata/package/testing/scripted::package-validation-script -> metadata/package/testing/scripted::package-validation-script
micro-behaviors/os/package-manager/install::multi-package-manager-install -> micro-behaviors/os/package-manager/install::multi-package-manager-install
objectives/impact/ransom/encrypt/runtime-generated::encrypted-outcome-reference -> metadata/lang/natural/vocabulary/content-word::encrypted-status-wording
objectives/lateral-movement/brute-force/password/appliance::netscaler-default-users--superadmin -> metadata/lang/source/naming/account::superadmin-word
objectives/lateral-movement/brute-force/password/web::sap-commerce-default-oauth-client-secret -> micro-behaviors/communications/http/oauth::placeholder-client-secret
objectives/lateral-movement/exploit/scanner::internal-cloud-probe-payload -> micro-behaviors/communications/http/services/cloud::cloud-metadata-host-reference
micro-behaviors/os/application/target/security::kasada-name-reference -> micro-behaviors/os/application/target/security::kasada-name-reference
micro-behaviors/os/application/target/security::perimeterx-name-reference -> micro-behaviors/os/application/target/security::perimeterx-name-reference
micro-behaviors/os/application/target/security::datadome-name-reference -> micro-behaviors/os/application/target/security::datadome-name-reference
micro-behaviors/os/application/target/security::imperva-name-reference -> micro-behaviors/os/application/target/security::imperva-name-reference
micro-behaviors/os/application/target/security::akamai-name-reference -> micro-behaviors/os/application/target/security::akamai-name-reference
micro-behaviors/os/application/target/security::shape-security-name-reference -> micro-behaviors/os/application/target/security::shape-security-name-reference
micro-behaviors/os/application/target/security::aws-waf-name-reference -> micro-behaviors/os/application/target/security::aws-waf-name-reference
micro-behaviors/os/application/target/security::recaptcha-name-reference -> micro-behaviors/os/application/target/security::recaptcha-name-reference
micro-behaviors/os/application/target/security::hcaptcha-name-reference -> micro-behaviors/os/application/target/security::hcaptcha-name-reference
micro-behaviors/os/application/target/security::arkose-name-reference -> micro-behaviors/os/application/target/security::arkose-name-reference
micro-behaviors/os/application/target/security::turnstile-name-reference -> micro-behaviors/os/application/target/security::turnstile-name-reference
micro-behaviors/os/application/target/security::geetest-name-reference -> micro-behaviors/os/application/target/security::geetest-name-reference
micro-behaviors/communications/http/cookie-name::cloudflare-clearance-reference -> micro-behaviors/communications/http/cookie-name::cloudflare-clearance-reference
micro-behaviors/communications/http/cookie-name::alibaba-acw-challenge-reference -> micro-behaviors/communications/http/cookie-name::alibaba-acw-challenge-reference
objectives/evasion/security-bypass/waf::multi-vendor-antibot-solvers -> micro-behaviors/os/application/target/security::multiple-bot-defense-vendor-references
objectives/evasion/security-bypass/waf::multi-captcha-provider-list -> micro-behaviors/os/application/target/security::multiple-captcha-provider-references
objectives/exfiltration/stealer/browser::macos-browser-cookie-store-http-exfil -> micro-behaviors/communications/http/cookie-store::macos-cookie-path-http-client
micro-behaviors/data/parse/vocabulary::browser-fingerprint-marker -> micro-behaviors/data/parse/vocabulary::browser-fingerprint-marker
micro-behaviors/data/parse/vocabulary::fingerprint-evasion-verb -> micro-behaviors/data/parse/vocabulary::fingerprint-evasion-verb
metadata/archive/member/size::archive-member-over-200kb -> metadata/archive/member/size::archive-member-over-200kb
metadata/archive/member/size::archive-member-under-10kb -> metadata/archive/member/size::archive-member-under-10kb
```

The original macos-browser-cookie-store-http-exfil ID is retained with stronger required evidence: cookie-path/HTTP capability, a dynamic DNS/public tunnel destination, and encoded-cookie outbound-body/pipe or file read/upload evidence. Its former neutral path/HTTP observation moves separately.
