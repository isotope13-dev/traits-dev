# Corpus observations

Tokenade 6.3.0: zero hostile, one suspicious vendor-evasion claim.
Tokenade 1.3.0: zero hostile and zero suspicious.

| Destination | Positive corpus member |
| --- | --- |
| `micro-behaviors/communications/http/cookie-store::chromium-encrypted-key-metadata` | `tokenade/core/crypto/cookie_crypto.py` |
| `micro-behaviors/data/db/sql::powershell-cookie-table-select` | Dependency or adjacent-case observation |
| `micro-behaviors/communications/http/cookie-store::chromium-cookie-query-with-browser-path` | Dependency or adjacent-case observation |
| `micro-behaviors/communications/http/cookie-store::browser-cookie-store-query` | Dependency or adjacent-case observation |
| `micro-behaviors/communications/http/devtools/client::cdp-discovered-cookie-jar-read` | `tokenade/cli/session.py` |
| `micro-behaviors/data/serialize/binary::python-pack-hex-u32` | `tokenade/tests/test_browser_support.py` |
| `micro-behaviors/os/message/queue::message-loop-string` | Dependency or adjacent-case observation |
| `micro-behaviors/communications/http/response::python-forbidden-status-argument` | `tokenade/core/proxy/cdp_gui.py` |
| `micro-behaviors/communications/http/response::drf-authorization-response` | Dependency or adjacent-case observation |
| `micro-behaviors/communications/http/user-agent::chrome-user-agent-script` | `tokenade/core/browser/battle.py` |
| `micro-behaviors/communications/http/url/domain::amazon-commerce-domain` | `tokenade/core/importer/site_configs.py` |
| `micro-behaviors/data/db/sql::browser-record-table-select` | `tokenade/core/injector/profile_manager.py` |
| `micro-behaviors/os/security/keychain::chrome-safe-storage-query` | `tokenade/core/crypto/cookie_crypto.py` |
| `micro-behaviors/os/security/dpapi::python-chromium-key-unprotect` | `tokenade/core/crypto/cookie_crypto.py` |
| `micro-behaviors/fs/path/application/browser::firefox-storage-database-reference` | Dependency or adjacent-case observation |
| `micro-behaviors/data/db/web-storage::auth-token-getitem-source` | `tokenade/handlers/generic_oauth.py` |
| `micro-behaviors/fs/path/cookie::firefox-cookies-sqlite-filename` | `tokenade/core/browser/profile_cloner.py` |
| `micro-behaviors/os/security/keychain::python-find-generic-password` | `tokenade/core/crypto/cookie_crypto.py` |
| `micro-behaviors/data/collection/wordlist::python-password-list-loop` | Dependency or adjacent-case observation |
| `micro-behaviors/data/db/write/row::last-checked-sql-assignment` | `tokenade/core/refresh/health_checker.py` |
| `micro-behaviors/ui/controls/credential::human-verification-marker` | Dependency or adjacent-case observation |
| `micro-behaviors/ui/controls/credential::browser-verification-status-text` | Dependency or adjacent-case observation |
| `micro-behaviors/fs/path/metadata-store::python-manifest-json-filename` | `tokenade/tests/test_profile_cloner.py` |
| `metadata/package/documentation/claims::browser-session-extraction-description` | `tokenade-6.3.0.dist-info/METADATA` |
| `metadata/package/documentation/claims::portable-browser-session-description` | Dependency or adjacent-case observation |
| `metadata/package/documentation/claims::donor-session-replay-description` | `tokenade-6.3.0.dist-info/METADATA` |
| `metadata/package/documentation/claims::package-advertises-browser-session-replay` | `tokenade-6.3.0.dist-info/METADATA` |
| `micro-behaviors/communications/http/cookie-name::apisid-sapisid-cookie-pair` | `tokenade/core/importer/cookie_extractor.py` |
| `micro-behaviors/communications/http/cookie-name::entra-session-cookie-name` | `tokenade/core/importer/site_configs.py` |
| `micro-behaviors/communications/http/cookie-name::microsoft-signin-state-cookie-name` | Dependency or adjacent-case observation |
| `micro-behaviors/communications/http/cookie-name::idp-session-cookie-named` | Dependency or adjacent-case observation |
| `micro-behaviors/communications/http/cookie-name::idp-session-cookie-targeting` | `tokenade/core/importer/site_configs.py` |
| `micro-behaviors/fs/path/application/browser::android-chromium-secret-store-path` | `tokenade/core/importer/adb_extractor.py` |
| `micro-behaviors/data/parse/vocabulary::token-extraction-wording` | `tokenade/cli/session.py` |
| `micro-behaviors/os/sysinfo/platform/browser::headlesschrome-string-test` | `tokenade/core/browser/stealth_test.py` |
| `micro-behaviors/os/sysinfo/platform/browser::nightmare-automation-global-reference` | `tokenade/core/browser/stealth/manager.py` |
| `micro-behaviors/os/sysinfo/platform/browser::chrome-automation-global-reference` | `tokenade/core/browser/stealth_test.py` |
| `micro-behaviors/os/sysinfo/platform/browser::callphantom-global-reference` | `tokenade/core/browser/stealth/manager.py` |
| `micro-behaviors/os/application/target::multiple-browser-names` | `tokenade/core/browser/stealth/launcher.py` |
| `metadata/file/naming::chromium-basename-word` | `tokenade/core/importer/chromium_forks.py` |
| `metadata/file/naming::safari-basename-word` | Dependency or adjacent-case observation |
| `micro-behaviors/fs/path/config/app::safari-preferences-plist` | Dependency or adjacent-case observation |
| `micro-behaviors/fs/path/personal::safari-history-db` | Dependency or adjacent-case observation |
| `micro-behaviors/fs/path/application/browser::safari-data-path-reference` | `tokenade/core/importer/mobile_extractor.py` |
| `micro-behaviors/fs/path/application/browser::chromium-profile-subdirectory-reference` | `tokenade/tests/test_chromium_forks_coverage.py` |
| `micro-behaviors/fs/path/application/browser::multiple-browser-data-references` | `tokenade/core/importer/mobile_extractor.py` |
| `micro-behaviors/communications/proxy/turn::webrtc-empty-ice-servers` | Dependency or adjacent-case observation |
| `micro-behaviors/communications/proxy/turn::local-ip-list-symbol` | Dependency or adjacent-case observation |
| `micro-behaviors/communications/proxy/turn::webrtc-local-ip-discovery` | `tokenade/core/fingerprint/collectors/webrtc.py` |
| `micro-behaviors/communications/http/header/accept::script-client-browser-header-pair` | `tokenade/core/runtime/engine.py` |
| `metadata/package/testing/scripted::package-validation-script` | Dependency or adjacent-case observation |
| `micro-behaviors/os/package-manager/install::multi-package-manager-install` | `tokenade/core/browser/xvfb.py` |
| `micro-behaviors/data/parse/vocabulary::encrypted-status-wording` | `tokenade/core/crypto/encryptor.py` |
| `micro-behaviors/os/user/account::superadmin-word` | `tokenade/tests/test_audit_coverage.py` |
| `micro-behaviors/communications/http/oauth::placeholder-client-secret` | `tokenade/tests/test_generic_oauth_coverage.py` |
| `micro-behaviors/communications/http/services/cloud::cloud-metadata-host-reference` | `tokenade/core/proxy/cdp_stealth.py` |
| `micro-behaviors/os/application/target::kasada-name-reference` | Dependency or adjacent-case observation |
| `micro-behaviors/os/application/target::perimeterx-name-reference` | Dependency or adjacent-case observation |
| `micro-behaviors/os/application/target::datadome-name-reference` | `tokenade-6.3.0.dist-info/METADATA` |
| `micro-behaviors/os/application/target::imperva-name-reference` | Dependency or adjacent-case observation |
| `micro-behaviors/os/application/target::akamai-name-reference` | `tokenade/core/browser/cloudflare.py` |
| `micro-behaviors/os/application/target::shape-security-name-reference` | Dependency or adjacent-case observation |
| `micro-behaviors/os/application/target::aws-waf-name-reference` | Dependency or adjacent-case observation |
| `micro-behaviors/os/application/target::recaptcha-name-reference` | `tokenade/core/browser/captcha.py` |
| `micro-behaviors/os/application/target::hcaptcha-name-reference` | `tokenade/core/browser/captcha.py` |
| `micro-behaviors/os/application/target::arkose-name-reference` | `tokenade/core/browser/captcha.py` |
| `micro-behaviors/os/application/target::turnstile-name-reference` | `tokenade/core/browser/battle.py` |
| `micro-behaviors/os/application/target::geetest-name-reference` | Dependency or adjacent-case observation |
| `micro-behaviors/communications/http/cookie-name::cloudflare-clearance-reference` | `tokenade/cli/__init__.py` |
| `micro-behaviors/communications/http/cookie-name::alibaba-acw-challenge-reference` | Dependency or adjacent-case observation |
| `micro-behaviors/os/application/target::multiple-bot-defense-vendor-references` | `tokenade-6.3.0.dist-info/METADATA` |
| `micro-behaviors/os/application/target::multiple-captcha-provider-references` | `tokenade/core/browser/captcha.py` |
| `micro-behaviors/communications/http/cookie-store::macos-cookie-path-http-client` | Dependency or adjacent-case observation |
| `micro-behaviors/data/parse/vocabulary::browser-fingerprint-marker` | `tokenade/__init__.py` |
| `micro-behaviors/data/parse/vocabulary::fingerprint-evasion-verb` | `tokenade/cli/advanced.py` |
| `metadata/file/archive::archive-member-over-200kb` | Dependency or adjacent-case observation |
| `metadata/file/archive::archive-member-under-10kb` | Dependency or adjacent-case observation |
