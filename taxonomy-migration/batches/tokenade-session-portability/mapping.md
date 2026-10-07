# Tokenade trait dispositions

Unlisted source IDs retain their original matcher and placement. Effective defaults are preserved. Intentional coverage changes are discussed in README.md.

```text
objectives/credential-access/browser/chromium::master-decrypt -> micro-behaviors/communications/http/cookie-store::chromium-encrypted-key-metadata
objectives/credential-access/browser/chromium::powershell-cookie-sql -> micro-behaviors/data/db/sql::powershell-cookie-table-select
objectives/credential-access/browser/chromium::cookie-theft -> micro-behaviors/communications/http/cookie-store::chromium-cookie-query-with-browser-path
objectives/credential-access/browser/session-hijack::browser-cookie-store-query -> micro-behaviors/communications/http/cookie-store::browser-cookie-store-query
objectives/credential-access/browser/devtools::chromium-cdp-discovered-cookie-harvest -> micro-behaviors/communications/http/devtools/client::cdp-discovered-cookie-jar-read
objectives/anti-static/obfuscation/encoding/ip-notation::ipv4-struct-pack -> micro-behaviors/data/serialize/binary::python-pack-hex-u32
objectives/collection/clipboard/monitor::message-loop-str -> micro-behaviors/os/message/queue::message-loop-string
objectives/command-and-control/backdoor/webshell/deny::drf-forbidden-status -> micro-behaviors/communications/http/response::python-forbidden-status-argument
objectives/command-and-control/backdoor/webshell/deny::drf-authorization-response-marker -> micro-behaviors/communications/http/response::drf-authorization-response
objectives/command-and-control/channel/http-beacon::chrome-spoof-user-agent-script -> micro-behaviors/communications/http/user-agent::chrome-user-agent-script
objectives/credential-access/browser/chromium::amazon-cookie-domain -> micro-behaviors/communications/http/url/domain::amazon-commerce-domain
objectives/credential-access/browser/chromium::browser-creds-table-sql -> micro-behaviors/data/db/sql::browser-record-table-select
objectives/credential-access/browser/chromium::chrome-safe-storage-keychain-query -> micro-behaviors/os/security/keychain::chrome-safe-storage-query
objectives/credential-access/browser/chromium::python-dpapi-browser-decrypt -> micro-behaviors/os/security/dpapi::python-chromium-key-unprotect
objectives/credential-access/browser/firefox::local-storage-access -> micro-behaviors/fs/path/application/browser::firefox-storage-database-reference
objectives/credential-access/browser/account-page::auth-storage-read-call -> micro-behaviors/data/db/web-storage::auth-token-getitem-source
objectives/credential-access/browser/session-hijack::jwt-file-or-browser-read--rx-1 -> micro-behaviors/fs/path/cookie::firefox-cookies-sqlite-filename
objectives/credential-access/keychain/extract::python-find-generic-password -> micro-behaviors/os/security/keychain::python-find-generic-password
objectives/credential-access/cracking/password::python-password-list-loop -> micro-behaviors/data/collection/wordlist::python-password-list-loop
objectives/credential-access/validation/check::last-checked-sql-assignment -> micro-behaviors/data/db/write/row::last-checked-sql-assignment
objectives/evasion/decoy/cloaking::js-fake-cloudflare -> micro-behaviors/ui/controls/credential::human-verification-marker
objectives/evasion/decoy/lure::browser-verification-interstitial -> micro-behaviors/ui/controls/credential::browser-verification-status-text
objectives/supply-chain/hidden-payload/native-extension::python-release-manifest-reference -> micro-behaviors/fs/path/metadata-store::python-manifest-json-filename
objectives/collection/app-data/session::browser-session-extraction-description -> metadata/package/documentation/claims::browser-session-extraction-description
objectives/collection/app-data/session::portable-browser-session-description -> metadata/package/documentation/claims::portable-browser-session-description
objectives/collection/app-data/session::donor-session-replay-description -> metadata/package/documentation/claims::donor-session-replay-description
objectives/collection/app-data/session::package-advertises-browser-session-replay -> metadata/package/documentation/claims::package-advertises-browser-session-replay
objectives/command-and-control/channel/http/message::apisid-sapisid-cookie-pair -> micro-behaviors/communications/http/cookie-name::apisid-sapisid-cookie-pair
objectives/credential-access/browser/session-hijack::entra-session-cookie-name -> micro-behaviors/communications/http/cookie-name::entra-session-cookie-name
objectives/credential-access/browser/session-hijack::microsoft-signin-state-cookie-name -> micro-behaviors/communications/http/cookie-name::microsoft-signin-state-cookie-name
objectives/credential-access/browser/session-hijack::idp-session-cookie-named -> micro-behaviors/communications/http/cookie-name::idp-session-cookie-named
objectives/credential-access/browser/session-hijack::idp-session-cookie-targeting -> micro-behaviors/communications/http/cookie-name::idp-session-cookie-targeting
objectives/credential-access/theft/file::android-browser-secret-path -> micro-behaviors/fs/path/application/browser::android-chromium-secret-store-path
objectives/credential-access/theft/keywords::token -> micro-behaviors/data/parse/vocabulary::token-extraction-wording
objectives/credential-access/phishing/landing::headlesschrome-match -> micro-behaviors/os/sysinfo/platform/browser::headlesschrome-string-test
objectives/anti-analysis/sandbox-detect/tool-references::js-phantom-nightmare-globals--rx-3 -> micro-behaviors/os/sysinfo/platform/browser::nightmare-automation-global-reference
objectives/anti-analysis/sandbox-detect/tool-references::js-phantom-nightmare-globals--rx-4 -> micro-behaviors/os/sysinfo/platform/browser::chrome-automation-global-reference
objectives/credential-access/wallet/mnemonic::phantom-word-unless-cond-1--rx-2 -> micro-behaviors/os/sysinfo/platform/browser::callphantom-global-reference
objectives/discovery/host/browser/identity::browser-names -> micro-behaviors/os/application/target::multiple-browser-names
objectives/discovery/host/browser/identity::chromium-binary-basename -> metadata/file/naming::chromium-basename-word
objectives/discovery/host/browser/identity::safari-binary-basename -> metadata/file/naming::safari-basename-word
objectives/discovery/host/browser/identity::safari-plist -> micro-behaviors/fs/path/config/app::safari-preferences-plist
objectives/discovery/host/browser/identity::safari-history-db -> micro-behaviors/fs/path/personal::safari-history-db
objectives/discovery/host/browser/identity::safari-history -> micro-behaviors/fs/path/application/browser::safari-data-path-reference
objectives/discovery/host/browser/identity::chromium-profile-subdirectory-reference -> micro-behaviors/fs/path/application/browser::chromium-profile-subdirectory-reference
objectives/discovery/host/browser/identity::multi-browser-enum -> micro-behaviors/fs/path/application/browser::multiple-browser-data-references
objectives/discovery/system/fingerprint/network::webrtc-empty-ice-servers -> micro-behaviors/communications/proxy/turn::webrtc-empty-ice-servers
objectives/discovery/system/fingerprint/network::local-ip-list-symbol -> micro-behaviors/communications/proxy/turn::local-ip-list-symbol
objectives/discovery/system/fingerprint/network::webrtc-local-ip-discovery -> micro-behaviors/communications/proxy/turn::webrtc-local-ip-discovery
objectives/evasion/masquerade/traffic::script-client-browser-header-pair -> micro-behaviors/communications/http/header/accept::script-client-browser-header-pair
objectives/execution/autoinstall/manager-package::package-validation-script -> metadata/package/testing/scripted::package-validation-script
objectives/execution/autoinstall/manager-package::multi-package-manager-install -> micro-behaviors/os/package-manager/install::multi-package-manager-install
objectives/impact/ransom/encrypt/runtime-generated::encrypted-outcome-reference -> micro-behaviors/data/parse/vocabulary::encrypted-status-wording
objectives/lateral-movement/brute-force/password/appliance::netscaler-default-users--superadmin -> micro-behaviors/os/user/account::superadmin-word
objectives/lateral-movement/brute-force/password/web::sap-commerce-default-oauth-client-secret -> micro-behaviors/communications/http/oauth::placeholder-client-secret
objectives/lateral-movement/exploit/scanner::internal-cloud-probe-payload -> micro-behaviors/communications/http/services/cloud::cloud-metadata-host-reference
objectives/evasion/security-bypass/waf::kasada-name-reference -> micro-behaviors/os/application/target::kasada-name-reference
objectives/evasion/security-bypass/waf::perimeterx-name-reference -> micro-behaviors/os/application/target::perimeterx-name-reference
objectives/evasion/security-bypass/waf::datadome-name-reference -> micro-behaviors/os/application/target::datadome-name-reference
objectives/evasion/security-bypass/waf::imperva-name-reference -> micro-behaviors/os/application/target::imperva-name-reference
objectives/evasion/security-bypass/waf::akamai-name-reference -> micro-behaviors/os/application/target::akamai-name-reference
objectives/evasion/security-bypass/waf::shape-security-name-reference -> micro-behaviors/os/application/target::shape-security-name-reference
objectives/evasion/security-bypass/waf::aws-waf-name-reference -> micro-behaviors/os/application/target::aws-waf-name-reference
objectives/evasion/security-bypass/waf::recaptcha-name-reference -> micro-behaviors/os/application/target::recaptcha-name-reference
objectives/evasion/security-bypass/waf::hcaptcha-name-reference -> micro-behaviors/os/application/target::hcaptcha-name-reference
objectives/evasion/security-bypass/waf::arkose-name-reference -> micro-behaviors/os/application/target::arkose-name-reference
objectives/evasion/security-bypass/waf::turnstile-name-reference -> micro-behaviors/os/application/target::turnstile-name-reference
objectives/evasion/security-bypass/waf::geetest-name-reference -> micro-behaviors/os/application/target::geetest-name-reference
objectives/evasion/security-bypass/waf::cloudflare-clearance-reference -> micro-behaviors/communications/http/cookie-name::cloudflare-clearance-reference
objectives/evasion/security-bypass/waf::alibaba-acw-challenge-reference -> micro-behaviors/communications/http/cookie-name::alibaba-acw-challenge-reference
objectives/evasion/security-bypass/waf::multi-vendor-antibot-solvers -> micro-behaviors/os/application/target::multiple-bot-defense-vendor-references
objectives/evasion/security-bypass/waf::multi-captcha-provider-list -> micro-behaviors/os/application/target::multiple-captcha-provider-references
objectives/exfiltration/stealer/browser::macos-browser-cookie-store-http-exfil -> micro-behaviors/communications/http/cookie-store::macos-cookie-path-http-client
objectives/evasion/security-bypass/anti-bot/fingerprint-spoof::browser-fingerprint-marker -> micro-behaviors/data/parse/vocabulary::browser-fingerprint-marker
objectives/evasion/security-bypass/anti-bot/fingerprint-spoof::fingerprint-evasion-verb -> micro-behaviors/data/parse/vocabulary::fingerprint-evasion-verb
metadata/file/naming::archive-member-over-200kb -> metadata/file/archive::archive-member-over-200kb
metadata/file/naming::archive-member-under-10kb -> metadata/file/archive::archive-member-under-10kb
```

The original macos-browser-cookie-store-http-exfil ID is retained with stronger required evidence: cookie-path/HTTP capability, a dynamic DNS/public tunnel destination, and encoded-cookie outbound-body/pipe or file read/upload evidence. Its former neutral path/HTTP observation moves separately.
