#!/usr/bin/env python3
"""Check VSIX techniques and benign controls without running extension code."""
import json
import os
from pathlib import Path
import subprocess
import shutil
import tempfile

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BRIDGE = 'objectives/command-and-control/reverse-shell/stream-bridge::node-socket-callback-shell-bridge'
ENCODED = 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-hidden-encoded-executable-stage'
PAIR = 'objectives/command-and-control/dropper/staging/native/payload::batch-temp-native-pair-background-stage'
PROFILE = 'objectives/exfiltration/stealer/system-info/profile::base64-env-profile-fetch-query'
STARTUP = 'objectives/supply-chain/recon-exfil/callback::vscode-startup-encoded-profile-query'
VULNERABLE = 'objectives/supply-chain/trojanized/app/ai-agent-tools::prompt-requests-vulnerable-code'
CASES = {
    'editor-root-native-bootstrap.vsix': {'require': ['objectives/command-and-control/dropper/staging/native/payload::activation-editor-root-native-bootstrap'], 'hostile_min': 2},
    'different-editor-root-launch.js': {'forbid': ['objectives/command-and-control/dropper/staging/native/payload::activation-editor-root-native-bootstrap']},
    'deferred-temp-batch.js': {'forbid': ['objectives/command-and-control/dropper/staging/script::import-time-hidden-temp-batch'], 'hostile_max': 0},
    'indirect-editor-installer.vsix': {'hostile_min': 3},
    'ordinary-multi-credential-config.js': {'require': ['micro-behaviors/os/env/config::node-several-credential-config-sources'], 'criticality_max': 3},
    'quoted-temp-batch.js': {'require': ['micro-behaviors/process/create/shell/command-string::cmd-curl-temp-batch-invocation', 'objectives/evasion/process/hidden/window::hidden-cmd-temp-batch-launch']},
    'different-quoted-temp-batch.js': {'forbid': ['micro-behaviors/process/create/shell/command-string::cmd-curl-temp-batch-invocation']},
    'variable-temp-batch.js': {'require': ['objectives/command-and-control/dropper/staging/script::import-time-hidden-temp-batch', 'micro-behaviors/process/create/shell/command-string::powershell-temp-batch-variable-invocation', 'objectives/evasion/process/hidden/window::hidden-powershell-temp-batch-launch']},
    'different-variable-temp-batch.js': {'forbid': ['micro-behaviors/process/create/shell/command-string::powershell-temp-batch-variable-invocation']},
    'packrat-carrier.vsix': {'require': ['well-known/malware/supply-chain/packrat::automatic-packrat-payload-installation'], 'hostile_min': 1},
    'ordinary-extension-pack.vsix': {'criticality_max': 3},
    'concealed-editor-installer.vsix': {'hostile_min': 3},
    'auth-identity-poc.vsix': {'require': ['objectives/credential-access/dev-tools/session::serializer-extension-identity-rewrite', 'objectives/credential-access/dev-tools/session::silent-auth-session-with-identity-rewrite'], 'suspicious_min': 2, 'hostile_max': 0},
    'ordinary-silent-session.js': {'criticality_max': 3},
    'ordinary-identity-migration.js': {'criticality_max': 3},
    'hidden-temp-batch.vsix': {'require': ['micro-behaviors/process/create/shell/command-string::powershell-curl-temp-batch-invocation', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-invisible-name-hidden-batch-stage'], 'hostile_min': 1},
    'different-temp-batch.js': {'forbid': ['micro-behaviors/process/create/shell/command-string::powershell-curl-temp-batch-invocation'], 'criticality_max': 3},
    'rc4-multiline-loader.js': {'require': ['micro-behaviors/crypto/symmetric/stream/rc4::js-rc4-implementation', 'objectives/anti-static/obfuscation/obfuscator/js-obfuscator::rc4-checksum-rotated-table-runtime']},
    'package.json': {'require': ['metadata/package/dependencies/manifest/identity::npm-declares-node-builtins-as-dependencies'], 'criticality_max': 3},
    'version-check-extension.vsix': {'criticality_max': 3},
    'fork-install-readme.vsix': {'criticality_max': 3},
    'routeros-client.js': {'criticality_max': 3},
    'native-abi-mismatch.vsix': {'suspicious_min': 2, 'hostile_max': 0},
    'ordinary-native-addon.node': {'criticality_max': 3},
    'fetch-arbitrary-target.js': {'require': ['micro-behaviors/communications/http/request/client::js-fetch-call'], 'criticality_max': 3},
    'fetch-syntax-data.js': {'forbid': ['micro-behaviors/communications/http/request/client::js-fetch-call'], 'criticality_max': 3},
    'filename-breakout-control.js': {'criticality_max': 3},
    'filename-breakout-positive.js': {'require': ['objectives/execution/exploit/command-injection::js-filename-quote-shell-breakout']},
    'response-vm-extension.vsix': {'hostile_min': 3},
    'ordinary-vm-http.js': {'criticality_max': 3},
    'decrypt-eval-positive.js': {'require': ['objectives/supply-chain/hidden-payload/encoding::aes-decrypt-eval-loader']},
    'unrelated-crypto-eval.js': {'criticality_max': 3},
    'hidden-python-stage.vsix': {'suspicious_min': 2, 'hostile_max': 0},
    'dormant-hidden-stage.vsix': {'suspicious_min': 2, 'hostile_max': 0},
    'wallet-archive-stealer.vsix': {'hostile_min': 3},
    'response-vm-loader.js': {'hostile_min': 1},
    'clipboard-hotkey-manager.py': {'criticality_max': 3},
    'dialog-key-webhook.vsix': {'require': ['objectives/exfiltration/messaging/discord::dialog-credential-discord-post'], 'hostile_min': 3},
    'event-shell.vsix': {'require': ['objectives/command-and-control/reverse-shell/stream-bridge::node-event-callback-shell-bridge'], 'hostile_min': 3},
    'named-host-shell.vsix': {'require': [BRIDGE], 'hostile_min': 3},
    'remote-agent.vsix': {'criticality_max': 3},
    'periodic-loader.vsix': {'require': ['objectives/command-and-control/beacon/network/periodic::periodic-http-response-eval'], 'hostile_min': 3},
    'legacy-api-parser.vsix': {'hostile_max': 0, 'suspicious_min': 1},
    'official-provider-client.vsix': {'criticality_max': 3},
    'socket-shell.vsix': {'require': [BRIDGE], 'hostile_min': 3},
    'encoded-downloader.vsix': {'require': [ENCODED], 'hostile_min': 1},
    'native-pair.vsix': {'require': [PAIR, 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-hidden-batch-native-pair-stage'], 'suspicious_min': 2},
    'profile-beacon.vsix': {'require': [PROFILE, STARTUP], 'suspicious_min': 2, 'hostile_max': 0},
    'security-policy.vsix': {'criticality_max': 3},
    'disclosed-provider.vsix': {'criticality_max': 3},
    'notification-helper.vsix': {'criticality_max': 3},
    'normal-dialog-webhook.js': {'criticality_max': 3},
    'socket-client.js': {'criticality_max': 3},
    'unrelated-streams.js': {'criticality_max': 3},
    'powershell-helper.js': {'criticality_max': 3},
    'ordinary-download.bat': {'criticality_max': 3, 'forbid': [PAIR]},
    'rejected-code-request.js': {'criticality_max': 3},
    'live-code-request.js': {'require': [VULNERABLE]},
    'mixed-code-request.js': {'require': [VULNERABLE]},
    'offline-xor-profile.js': {'criticality_max': 3},
    'encrypted-job-broker.vsix': {'hostile_min': 3, 'require': ['objectives/command-and-control/backdoor/control/job-broker::encrypted-hidden-command-job-broker', 'objectives/execution/compile/runtime::encrypted-job-broker-csharp-script-host']},
    'different-host-codec-key.js': {'forbid': ['micro-behaviors/data/encode/xor::host-identity-compressed-xor-codec']},
    'different-child-input.js': {'forbid': ['micro-behaviors/process/io/stdin::function-input-hidden-child-stdin', 'objectives/command-and-control/backdoor/control/job-broker::encrypted-hidden-command-job-broker']},
    'boolean-hidden-child.js': {'require': ['micro-behaviors/process/io/stdin::function-input-hidden-child-stdin', 'objectives/command-and-control/backdoor/control/job-broker::encrypted-hidden-command-job-broker'], 'hostile_min': 1},
    'ordinary-quoted-command-chain.js': {'criticality_max': 3},
    'xampp-current.js': {'require': ['objectives/credential-access/messaging/whatsapp::whatsapp-pairing-qr-remote-renderer', 'objectives/execution/exploit/command-injection::messaging-body-unquoted-shell-argument'], 'suspicious_min': 2, 'hostile_max': 0},
    'xampp-previous.js': {'require': ['objectives/credential-access/messaging/whatsapp::whatsapp-pairing-qr-remote-renderer', 'objectives/execution/exploit/command-injection::messaging-body-unquoted-shell-argument'], 'suspicious_min': 2, 'hostile_max': 0},
    'message-execfile-arguments.js': {'require': ['objectives/credential-access/messaging/whatsapp::whatsapp-pairing-qr-remote-renderer'], 'forbid': ['objectives/execution/exploit/command-injection::messaging-body-unquoted-shell-argument'], 'hostile_max': 0},
    'pairing-local-renderer.js': {'require': ['objectives/execution/exploit/command-injection::messaging-body-unquoted-shell-argument'], 'forbid': ['objectives/credential-access/messaging/whatsapp::whatsapp-pairing-qr-remote-renderer'], 'hostile_max': 0},
    'public-qr-data.js': {'require': ['objectives/execution/exploit/command-injection::messaging-body-unquoted-shell-argument'], 'forbid': ['objectives/credential-access/messaging/whatsapp::whatsapp-pairing-qr-remote-renderer'], 'hostile_max': 0},
    'agent-branding-prompt.js': {'criticality_max': 3},
    'concealed-action-with-branding.js': {'require': ['objectives/evasion/security-bypass/llm/prompt/override::repository-content-agent-prompt-injection'], 'suspicious_min': 1},
    'credential-gated-runner.js': {'require': ['objectives/execution/autoinstall/credential-gate::credential-probes-gate-remote-package-runner', 'objectives/execution/autoinstall/manager-package::credential-gated-multi-runner-package-execution', 'micro-behaviors/os/package-manager/run::parallel-results-gate-url-runner-handler'], 'hostile_min': 2},
    'credential-gated-runner.vsix': {'require': ['objectives/execution/autoinstall/credential-gate::credential-probes-gate-remote-package-runner', 'objectives/execution/autoinstall/manager-package::credential-gated-multi-runner-package-execution', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-startup-credential-gated-package-runner'], 'hostile_min': 3},
    'renamed-credential-runner.js': {'require': ['objectives/execution/autoinstall/credential-gate::credential-probes-gate-remote-package-runner', 'objectives/execution/autoinstall/manager-package::credential-gated-multi-runner-package-execution', 'micro-behaviors/os/package-manager/run::parallel-results-gate-url-runner-handler'], 'hostile_min': 2},
    'reordered-credential-runner.js': {'require': ['objectives/execution/autoinstall/credential-gate::credential-probes-gate-remote-package-runner', 'micro-behaviors/os/package-manager/run::parallel-results-gate-url-runner-handler'], 'hostile_min': 2},
    'unrelated-gated-handler.js': {'forbid': ['micro-behaviors/os/package-manager/run::parallel-results-gate-url-runner-handler', 'objectives/execution/autoinstall/credential-gate::credential-probes-gate-remote-package-runner', 'objectives/execution/autoinstall/manager-package::credential-gated-multi-runner-package-execution', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-startup-credential-gated-package-runner'], 'hostile_max': 0},
    'different-runner-exec-input.js': {'forbid': ['micro-behaviors/os/package-manager/run::parallel-results-gate-url-runner-handler', 'objectives/execution/autoinstall/credential-gate::credential-probes-gate-remote-package-runner', 'objectives/execution/autoinstall/manager-package::credential-gated-multi-runner-package-execution', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-startup-credential-gated-package-runner'], 'hostile_max': 0},
    'version-gated-package-installer.js': {'require': ['micro-behaviors/os/package-manager/run::parallel-results-gate-url-runner-handler'], 'criticality_max': 3},
    'ci-tool-discovery-design.md': {'criticality_max': 3},
    'design-with-concealed-upload.md': {'require': ['objectives/evasion/security-bypass/llm/prompt/override::repository-content-agent-prompt-injection'], 'suspicious_min': 1},
    'registry-api-reference-catalog.py': {'require': ['micro-behaviors/os/registry/offline-hive::offreg-hive-write-api-context'], 'criticality_max': 3},
    'imds-path-reference-catalog.js': {'require': ['metadata/lang/source/shape::module-call-and-imds-path-context'], 'criticality_max': 3},
    'skill-content-catalog.js': {'forbid': ['objectives/command-and-control/backdoor/rat/command-set::windows-rat-domain-takeover-tasking', 'objectives/credential-access/cloud/token/metadata::npm-load-time-imds-token-role-recon', 'objectives/command-and-control/backdoor/webshell/embedded::embedded-wordpress-plugin-command-webshell'], 'require': ['micro-behaviors/data/embedded/script::wordpress-request-execution-fragment-context']},
    'administration-name-catalog.js': {'require': ['metadata/lang/source/naming/action::ad-user-name-tokens', 'metadata/lang/source/naming/action::network-scan-name-tokens'], 'criticality_max': 3},
    'native-import-iife.vsix': {'require': ['micro-behaviors/os/module/require::silent-exportless-native-import-iife', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-startup-native-abi-mismatch'], 'suspicious_min': 2, 'hostile_max': 0},
    'native-import-iife.js': {'require': ['micro-behaviors/os/module/require::silent-exportless-native-import-iife'], 'suspicious_min': 1, 'hostile_max': 0},
    'native-iife-binding-variant.js': {'require': ['micro-behaviors/os/module/require::silent-exportless-native-import-iife'], 'suspicious_min': 1, 'hostile_max': 0},
    'different-iife-native-input.js': {'forbid': ['micro-behaviors/os/module/require::silent-exportless-native-import-iife'], 'criticality_max': 3},
    'shadowed-native-require.js': {'forbid': ['micro-behaviors/os/module/require::silent-exportless-native-import-iife'], 'criticality_max': 3},
    'deferred-native-import.js': {'forbid': ['micro-behaviors/os/module/require::silent-exportless-native-import-iife'], 'criticality_max': 3},
    'nx-compromised-bootstrap.js': {'require': ['well-known/malware/supply-chain/teampcp-nx::nx-console-teampcp-github-bootstrap'], 'hostile_min': 1},
    'different-github-commit-task.js': {'forbid': ['well-known/malware/supply-chain/teampcp-nx::nx-console-teampcp-github-bootstrap', 'well-known/malware/supply-chain/teampcp-nx::compromised-bootstrap-commit-reference'], 'hostile_max': 0},
    'quoted-bootstrap-reference.js': {'forbid': ['well-known/malware/supply-chain/teampcp-nx::nx-console-teampcp-github-bootstrap'], 'hostile_max': 0},
    'embedded-bootstrap-example.js': {'require': ['well-known/malware/supply-chain/teampcp-nx::compromised-bootstrap-commit-reference'], 'forbid': ['well-known/malware/supply-chain/teampcp-nx::nx-console-teampcp-github-bootstrap'], 'criticality_max': 3},
    'arrow-native-import.js': {'require': ['micro-behaviors/os/module/require::silent-exportless-native-import-iife'], 'suspicious_min': 1, 'hostile_max': 0},
    'generator-native-reference.js': {'forbid': ['micro-behaviors/os/module/require::silent-exportless-native-import-iife'], 'criticality_max': 3},
    'unreachable-native-iife.js': {'forbid': ['micro-behaviors/os/module/require::silent-exportless-native-import-iife'], 'criticality_max': 3},
    'xor-native-file-opener.js': {'require': ['micro-behaviors/process/create/shellexec::xor-buffer-http-native-file-open', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-xor-native-file-open'], 'hostile_min': 1},
    'different-native-open-path.js': {'forbid': ['micro-behaviors/process/create/shellexec::xor-buffer-http-native-file-open', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-xor-native-file-open'], 'hostile_max': 0},
    'ordinary-pdf-file-opener.js': {'forbid': ['micro-behaviors/process/create/shellexec::xor-buffer-http-native-file-open', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-xor-native-file-open'], 'hostile_max': 0},
    'non-xor-native-url.js': {'forbid': ['micro-behaviors/process/create/shellexec::xor-buffer-http-native-file-open', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-xor-native-file-open'], 'hostile_max': 0},
    'shadowed-file-opener-callback.js': {'forbid': ['micro-behaviors/process/create/shellexec::xor-buffer-http-native-file-open', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-xor-native-file-open'], 'hostile_max': 0},
    'unreachable-native-opener.js': {'forbid': ['micro-behaviors/process/create/shellexec::xor-buffer-http-native-file-open', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-xor-native-file-open'], 'hostile_max': 0},
    'unreachable-http-file-pipe.js': {'forbid': ['micro-behaviors/process/create/shellexec::xor-buffer-http-native-file-open', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-xor-native-file-open'], 'hostile_max': 0},
    'nonterminating-native-url-loop.js': {'forbid': ['micro-behaviors/process/create/shellexec::xor-buffer-http-native-file-open', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-xor-native-file-open'], 'hostile_max': 0},
    'changed-xor-native-file-opener.js': {'require': ['micro-behaviors/process/create/shellexec::xor-buffer-http-native-file-open', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-xor-native-file-open'], 'hostile_min': 1},
    'user-triggered-native-opener.js': {'forbid': ['micro-behaviors/process/create/shellexec::xor-buffer-http-native-file-open', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-xor-native-file-open'], 'hostile_max': 0},
    'xor-native-file-opener.vsix': {'require': ['objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-xor-native-file-open'], 'hostile_min': 1},

    'branding-underlying-model-comment.js': {'criticality_max': 3},
    'branding-model-identity-variants.js': {'criticality_max': 3},
    'novel-model-branding.md': {'criticality_max': 3},
    'concealed-upload-with-model-branding.md': {'require': ['objectives/evasion/security-bypass/llm/prompt/override::repository-content-agent-prompt-injection'], 'suspicious_min': 1},

    'privacy-credential-guardrail.md': {'criticality_max': 3},

    'crypto-name-and-rpc-reference.js': {'require': ['metadata/lang/source/shape::gost-proxy-vocabulary-context'], 'criticality_max': 3},
    'gost-proxy-command-reference.js': {'require': ['metadata/lang/source/shape::gost-proxy-vocabulary-context', 'metadata/lang/source/syntax/command::gost-listener-flag-source', 'metadata/lang/source/syntax/command::gost-forward-flag-source'], 'criticality_max': 3},
    'ordinary-grpc-reference.js': {'forbid': ['metadata/lang/source/shape::gost-proxy-vocabulary-context'], 'criticality_max': 3},
    'python-standalone-release-reference.js': {'require': ['metadata/lang/source/shape::python-standalone-release-marker-context'], 'criticality_max': 3},
    'distant-python-release-markers.js': {'forbid': ['metadata/lang/source/shape::python-standalone-release-marker-context'], 'criticality_max': 3},
    'debugger-event-api-set.exe': {'require': ['micro-behaviors/process/debug/event::debugger-attach-event-api-profile'], 'forbid': ['objectives/anti-analysis/debugger-detect/hardware-breakpoints::debugger-attach-loop']},
    'insecure-network-client.vsix': {'require': ['metadata/lang/source/shape::startup-extension-tls-ssh-verification-context', 'micro-behaviors/communications/tls/verify/disable::node-tls-verification-env-disable'], 'hostile_max': 0, 'suspicious_min': 1, 'suspicious_max': 1},
    'tls-only-client.vsix': {'forbid': ['metadata/lang/source/shape::startup-extension-tls-ssh-verification-context'], 'require': ['micro-behaviors/communications/tls/verify/disable::node-tls-verification-env-disable'], 'hostile_max': 0, 'suspicious_min': 1, 'suspicious_max': 1},

    'debugger-minidump-api-set.exe': {'require': ['micro-behaviors/process/debug/event::debugger-attach-event-api-profile', 'micro-behaviors/process/debug/dump::minidump-debug-helper'], 'forbid': ['objectives/anti-analysis/debugger-detect/hardware-breakpoints::debugger-attach-loop']},
    'documented-install-id-context.vsix': {'require': ['metadata/lang/source/shape::startup-extension-host-http-write-context'], 'criticality_max': 3},
    'local-install-id-context.vsix': {'forbid': ['metadata/lang/source/shape::startup-extension-host-http-write-context'], 'criticality_max': 3},

    'http-jscript-stage.js': {'require': ['micro-behaviors/process/create/shell/script-host::activation-http-temp-jscript-command', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-http-jscript-stage'], 'hostile_min': 1},
    'changed-http-jscript-stage.js': {'require': ['micro-behaviors/process/create/shell/script-host::activation-http-temp-jscript-command', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-http-jscript-stage'], 'hostile_min': 1},
    'different-jscript-command-path.js': {'forbid': ['micro-behaviors/process/create/shell/script-host::activation-http-temp-jscript-command', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-http-jscript-stage'], 'hostile_max': 0},
    'different-jscript-writer-path.js': {'forbid': ['micro-behaviors/process/create/shell/script-host::activation-http-temp-jscript-command', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-http-jscript-stage'], 'hostile_max': 0},
    'nonawait-jscript-stage.js': {'forbid': ['micro-behaviors/process/create/shell/script-host::activation-http-temp-jscript-command', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-http-jscript-stage'], 'hostile_max': 0},
    'nonjscript-stage.js': {'forbid': ['micro-behaviors/process/create/shell/script-host::activation-http-temp-jscript-command', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-http-jscript-stage'], 'hostile_max': 0},
    'early-return-jscript-stage.js': {'forbid': ['micro-behaviors/process/create/shell/script-host::activation-http-temp-jscript-command', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-http-jscript-stage'], 'hostile_max': 0},
    'shadowed-jscript-finish.js': {'forbid': ['micro-behaviors/process/create/shell/script-host::activation-http-temp-jscript-command', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-http-jscript-stage'], 'hostile_max': 0},
    'user-command-jscript-stage.js': {'forbid': ['micro-behaviors/process/create/shell/script-host::activation-http-temp-jscript-command', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-http-jscript-stage'], 'hostile_max': 0},
    'http-jscript-stage.vsix': {'require': ['objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-http-jscript-stage'], 'hostile_min': 1},

    'joined-encrypted-module.vsix': {'require': ['objectives/command-and-control/infrastructure/blockchain/solana::solana-memo-deaddrop-c2'], 'hostile_min': 2},
    'renamed-joined-encrypted-module.js': {'require': ['objectives/command-and-control/infrastructure/blockchain/solana::solana-memo-deaddrop-c2'], 'hostile_min': 2},
    'authentic-text-transform-extension.vsix': {'criticality_max': 3},

    'promised-http-jscript-stage.js': {'require': ['micro-behaviors/process/create/shell/script-host::activation-http-temp-jscript-command', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-http-jscript-stage'], 'hostile_min': 1},
    'changed-promised-http-jscript-stage.js': {'require': ['micro-behaviors/process/create/shell/script-host::activation-http-temp-jscript-command', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-http-jscript-stage'], 'hostile_min': 1},
    'different-promised-jscript-path.js': {'forbid': ['micro-behaviors/process/create/shell/script-host::activation-http-temp-jscript-command', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-http-jscript-stage'], 'hostile_max': 0},
    'different-download-promise.js': {'forbid': ['micro-behaviors/process/create/shell/script-host::activation-http-temp-jscript-command', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-http-jscript-stage'], 'hostile_max': 0},
    'shadowed-promise-completion.js': {'forbid': ['micro-behaviors/process/create/shell/script-host::activation-http-temp-jscript-command', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-http-jscript-stage'], 'hostile_max': 0},
    'early-return-promised-jscript.js': {'forbid': ['micro-behaviors/process/create/shell/script-host::activation-http-temp-jscript-command', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-http-jscript-stage'], 'hostile_max': 0},
    'deferred-jscript-promise.js': {'forbid': ['micro-behaviors/process/create/shell/script-host::activation-http-temp-jscript-command', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-http-jscript-stage'], 'hostile_max': 0},
    'nonjscript-promise-stage.js': {'forbid': ['micro-behaviors/process/create/shell/script-host::activation-http-temp-jscript-command', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-http-jscript-stage'], 'hostile_max': 0},
    'user-command-jscript-promise.js': {'forbid': ['micro-behaviors/process/create/shell/script-host::activation-http-temp-jscript-command', 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-http-jscript-stage'], 'hostile_max': 0},
    'edge-js-remote-injection.js': {'require': ['objectives/evasion/process/injection/memory::source-remote-thread-injection'], 'hostile_min': 1},
    'renamed-edge-js-remote-injection.js': {'require': ['objectives/evasion/process/injection/memory::source-remote-thread-injection'], 'hostile_min': 1},
    'benign-edge-js-bridge.js': {'forbid': ['objectives/evasion/process/injection/memory::source-remote-thread-injection'], 'hostile_max': 0, 'criticality_max': 3},
    'ordinary-js-comment-with-csharp.js': {'forbid': ['objectives/evasion/process/injection/memory::source-remote-thread-injection'], 'hostile_max': 0},
    'escaped-edge-js-bridge.js': {'forbid': ['objectives/evasion/process/injection/memory::source-remote-thread-injection'], 'hostile_max': 0},
    'shadowed-edge-js-require.js': {'forbid': ['objectives/evasion/process/injection/memory::source-remote-thread-injection'], 'hostile_max': 0},
    'promised-jscript-stage.vsix': {'require': ['objectives/supply-chain/hidden-payload/extensions/vscode::vscode-activation-http-jscript-stage'], 'hostile_min': 1},
    'edge-js-injection.vsix': {'require': ['objectives/evasion/process/injection/memory::source-remote-thread-injection'], 'hostile_min': 1},

    'terminal-table-escape.js': {'require': ['well-known/malware/supply-chain/glassworm::github-vsix-payload-url', 'well-known/malware/supply-chain/glassworm::obfuscated-vsix-loader-configuration'], 'hostile_min': 1},
    'renamed-terminal-table-escape.js': {'require': ['well-known/malware/supply-chain/glassworm::github-vsix-payload-url', 'well-known/malware/supply-chain/glassworm::obfuscated-vsix-loader-configuration'], 'hostile_min': 1},
    'changed-terminal-table-address.js': {'forbid': ['well-known/malware/supply-chain/glassworm::obfuscated-vsix-loader-configuration'], 'hostile_max': 0},
    'early-table-producer-escape.js': {'forbid': ['well-known/malware/supply-chain/glassworm::obfuscated-vsix-loader-configuration'], 'hostile_max': 0},
    'documented-glassworm-url.js': {'forbid': ['well-known/malware/supply-chain/glassworm::obfuscated-vsix-loader-configuration'], 'hostile_max': 0, 'require': ['well-known/malware/supply-chain/glassworm::github-vsix-payload-url'], 'criticality_max': 3},
    'formatter-prefix-source.vsix': {'require': ['well-known/malware/supply-chain/glassworm::github-vsix-payload-url', 'well-known/malware/supply-chain/glassworm::obfuscated-vsix-loader-configuration'], 'hostile_min': 1},

    'hidden-downloaded-file.js': {'hostile_max': 0, 'require': ['micro-behaviors/process/create/local-exec::activation-hidden-downloaded-file-launch', 'objectives/evasion/indicator-removal/cleanup::node-hidden-stage-timer-cleanup'], 'forbid': [], 'suspicious_min': 2},
    'renamed-hidden-downloaded-file.js': {'hostile_max': 0, 'require': ['micro-behaviors/process/create/local-exec::activation-hidden-downloaded-file-launch', 'objectives/evasion/indicator-removal/cleanup::node-hidden-stage-timer-cleanup'], 'forbid': [], 'suspicious_min': 2},
    'different-cleanup-file.js': {'hostile_max': 0, 'require': ['micro-behaviors/process/create/local-exec::activation-hidden-downloaded-file-launch'], 'forbid': ['objectives/evasion/indicator-removal/cleanup::node-hidden-stage-timer-cleanup']},
    'different-executed-download.js': {'hostile_max': 0, 'require': [], 'forbid': ['micro-behaviors/process/create/local-exec::activation-hidden-downloaded-file-launch', 'objectives/evasion/indicator-removal/cleanup::node-hidden-stage-timer-cleanup']},
    'shadowed-download-response.js': {'hostile_max': 0, 'require': [], 'forbid': ['micro-behaviors/process/create/local-exec::activation-hidden-downloaded-file-launch', 'objectives/evasion/indicator-removal/cleanup::node-hidden-stage-timer-cleanup']},
    'unreachable-hidden-download.js': {'hostile_max': 0, 'require': [], 'forbid': ['micro-behaviors/process/create/local-exec::activation-hidden-downloaded-file-launch', 'objectives/evasion/indicator-removal/cleanup::node-hidden-stage-timer-cleanup']},
    'deferred-hidden-download.js': {'hostile_max': 0, 'require': [], 'forbid': ['micro-behaviors/process/create/local-exec::activation-hidden-downloaded-file-launch', 'objectives/evasion/indicator-removal/cleanup::node-hidden-stage-timer-cleanup']},
    'different-hidden-writer.js': {'hostile_max': 0, 'require': [], 'forbid': ['micro-behaviors/process/create/local-exec::activation-hidden-downloaded-file-launch', 'objectives/evasion/indicator-removal/cleanup::node-hidden-stage-timer-cleanup']},
    'unexported-hidden-launcher.js': {'hostile_max': 0, 'require': [], 'forbid': ['micro-behaviors/process/create/local-exec::activation-hidden-downloaded-file-launch', 'objectives/evasion/indicator-removal/cleanup::node-hidden-stage-timer-cleanup']},
    'azure-identity-request-context.js': {'criticality_max': 3, 'require': ['metadata/lang/source/shape::azure-imds-identity-request-context']},
    'ordinary-provider-metadata.js': {'criticality_max': 3, 'forbid': ['metadata/lang/source/shape::azure-imds-identity-request-context']},
    'independent-debug-tty-exit.js': {'criticality_max': 3, 'require': ['metadata/lang/source/shape::node-inspect-tty-exit-context']},
    'tty-exit-without-inspect.js': {'criticality_max': 3, 'forbid': ['metadata/lang/source/shape::node-inspect-tty-exit-context']},
    'independent-workspace-file-operations.js': {'criticality_max': 3, 'require': ['metadata/lang/source/shape::vscode-workspace-edit-copy-unlink-context']},
    'workspace-operations-without-unlink.js': {'criticality_max': 3, 'forbid': ['metadata/lang/source/shape::vscode-workspace-edit-copy-unlink-context']},
    'hex-named-archive-member.vsix': {'criticality_max': 3, 'require': ['metadata/file/archive::high-entropy-hex-named-member-context']},
    'ordinary-archive-member.vsix': {'criticality_max': 3, 'forbid': ['metadata/file/archive::high-entropy-hex-named-member-context']},
    'renamed-bound-js-debugger-tty-gated-exit.js': {'suspicious_min': 1, 'hostile_max': 0, 'require': ['objectives/anti-analysis/self-terminate::js-debugger-tty-gated-exit']},
    'renamed-bound-debug-tty-gated-exit.js': {'suspicious_min': 1, 'hostile_max': 0, 'require': ['objectives/anti-analysis/self-terminate::js-debugger-tty-gated-exit']},
    'non-tty-only-exit.js': {'criticality_max': 3, 'forbid': ['objectives/anti-analysis/self-terminate::js-debugger-tty-gated-exit']},
    'debugger-only-exit.js': {'criticality_max': 3, 'forbid': ['objectives/anti-analysis/self-terminate::js-debugger-tty-gated-exit']},
    'hex-response-command-loader.js': {'require': ['objectives/command-and-control/remote-command/tasking::webpack-json-hex-shell-loader'], 'hostile_min': 1},
    'renamed-hex-response-command.js': {'require': ['objectives/command-and-control/remote-command/tasking::webpack-json-hex-shell-loader'], 'hostile_min': 1},
    'unguarded-hex-response-command.js': {'require': ['objectives/command-and-control/remote-command/tasking::webpack-json-hex-shell-loader'], 'hostile_min': 1},
    'quiet-hex-response-command.js': {'require': ['objectives/command-and-control/remote-command/tasking::webpack-json-hex-shell-loader'], 'hostile_min': 1},
    'direct-hex-response-command.js': {'require': ['objectives/command-and-control/remote-command/tasking::webpack-json-hex-shell-loader'], 'hostile_min': 1},
    'different-hex-response-exec-argument.js': {'forbid': ['objectives/command-and-control/remote-command/tasking::webpack-json-hex-shell-loader']},
    'different-json-response-buffer.js': {'forbid': ['objectives/command-and-control/remote-command/tasking::webpack-json-hex-shell-loader']},
    'different-http-response-chunk.js': {'forbid': ['objectives/command-and-control/remote-command/tasking::webpack-json-hex-shell-loader']},
    'different-response-exec-namespace.js': {'forbid': ['objectives/command-and-control/remote-command/tasking::webpack-json-hex-shell-loader']},
    'nonhex-response-decoder.js': {'forbid': ['objectives/command-and-control/remote-command/tasking::webpack-json-hex-shell-loader']},
    'nonterminating-response-decoder.js': {'forbid': ['objectives/command-and-control/remote-command/tasking::webpack-json-hex-shell-loader']},
    'unreachable-response-command.js': {'forbid': ['objectives/command-and-control/remote-command/tasking::webpack-json-hex-shell-loader']},
    'shadowed-response-exec-binding.js': {'forbid': ['objectives/command-and-control/remote-command/tasking::webpack-json-hex-shell-loader']},
    'nonprocess-response-module.js': {'forbid': ['objectives/command-and-control/remote-command/tasking::webpack-json-hex-shell-loader']},
    'nonhttp-response-module.js': {'forbid': ['objectives/command-and-control/remote-command/tasking::webpack-json-hex-shell-loader']},
    'different-last-response-call.js': {'forbid': ['objectives/command-and-control/remote-command/tasking::webpack-json-hex-shell-loader']},
    'changed-response-interop.js': {'forbid': ['objectives/command-and-control/remote-command/tasking::webpack-json-hex-shell-loader']},
    'documented-hex-response-source.js': {'forbid': ['objectives/command-and-control/remote-command/tasking::webpack-json-hex-shell-loader']},
    'hex-response-loader.vsix': {'require': ['objectives/command-and-control/remote-command/tasking::webpack-json-hex-shell-loader'], 'hostile_min': 1},
    'visible-agent-setting-descriptions.json': {'criticality_max': 3},
    'benchmark-decode-filename.package.json': {'criticality_max': 3},
    'timestamp-hook-filename.cmd': {'criticality_max': 3},
    'explicit-agent-review-bypass.md': {'require': ['objectives/evasion/security-bypass/llm/prompt/override::repository-content-agent-prompt-injection'], 'suspicious_min': 1},
    'unaddressed-review-wording.md': {'criticality_max': 3},
    'immutable-quoted-loader.js': {'criticality_max': 3},
    'long-name-batch-substrings.cmd': {'criticality_max': 3, 'require': ['micro-behaviors/data/string/access::batch-long-name-delayed-substring']},
    'short-name-batch-substrings.cmd': {'criticality_max': 3, 'require': ['micro-behaviors/data/string/access::batch-short-name-delayed-substring']},
    'decoded-response-global-hook.js': {'require': ['micro-behaviors/process/create/local-exec::activation-decoded-response-helper', 'micro-behaviors/process/create/shell/git::global-hook-background-helper', 'objectives/persistence/system/git-hooks::decoded-response-global-hook-persistence'], 'forbid': [], 'hostile_min': 1},
    'renamed-response-global-hook.js': {'require': ['micro-behaviors/process/create/local-exec::activation-decoded-response-helper', 'micro-behaviors/process/create/shell/git::global-hook-background-helper', 'objectives/persistence/system/git-hooks::decoded-response-global-hook-persistence'], 'forbid': [], 'hostile_min': 1},
    'changed-response-stage-buffer.js': {'require': [], 'forbid': ['micro-behaviors/process/create/local-exec::activation-decoded-response-helper', 'micro-behaviors/process/create/shell/git::global-hook-background-helper', 'objectives/persistence/system/git-hooks::decoded-response-global-hook-persistence'], 'hostile_max': 0},
    'changed-response-executed-path.js': {'require': [], 'forbid': ['micro-behaviors/process/create/local-exec::activation-decoded-response-helper', 'micro-behaviors/process/create/shell/git::global-hook-background-helper', 'objectives/persistence/system/git-hooks::decoded-response-global-hook-persistence'], 'hostile_max': 0},
    'changed-response-json-buffer.js': {'require': ['micro-behaviors/process/create/shell/git::global-hook-background-helper'], 'forbid': ['micro-behaviors/process/create/local-exec::activation-decoded-response-helper', 'objectives/persistence/system/git-hooks::decoded-response-global-hook-persistence'], 'hostile_max': 0},
    'changed-response-helper-return.js': {'require': ['micro-behaviors/process/create/shell/git::global-hook-background-helper'], 'forbid': ['micro-behaviors/process/create/local-exec::activation-decoded-response-helper', 'objectives/persistence/system/git-hooks::decoded-response-global-hook-persistence'], 'hostile_max': 0},
    'nonbase64-response-helper.js': {'require': ['micro-behaviors/process/create/shell/git::global-hook-background-helper'], 'forbid': ['micro-behaviors/process/create/local-exec::activation-decoded-response-helper', 'objectives/persistence/system/git-hooks::decoded-response-global-hook-persistence'], 'hostile_max': 0},
    'response-helper-early-return.js': {'require': [], 'forbid': ['micro-behaviors/process/create/local-exec::activation-decoded-response-helper', 'micro-behaviors/process/create/shell/git::global-hook-background-helper', 'objectives/persistence/system/git-hooks::decoded-response-global-hook-persistence'], 'hostile_max': 0},
    'response-helper-no-activation.js': {'require': [], 'forbid': ['micro-behaviors/process/create/local-exec::activation-decoded-response-helper', 'micro-behaviors/process/create/shell/git::global-hook-background-helper', 'objectives/persistence/system/git-hooks::decoded-response-global-hook-persistence'], 'hostile_max': 0},
    'response-helper-no-global-hook.js': {'require': ['micro-behaviors/process/create/local-exec::activation-decoded-response-helper'], 'forbid': ['micro-behaviors/process/create/shell/git::global-hook-background-helper', 'objectives/persistence/system/git-hooks::decoded-response-global-hook-persistence'], 'hostile_max': 0},
    'response-helper-wrong-hook-command.js': {'require': ['micro-behaviors/process/create/local-exec::activation-decoded-response-helper'], 'forbid': ['micro-behaviors/process/create/shell/git::global-hook-background-helper', 'objectives/persistence/system/git-hooks::decoded-response-global-hook-persistence'], 'hostile_max': 0},
    'response-helper-other-hook-path.js': {'require': ['micro-behaviors/process/create/local-exec::activation-decoded-response-helper'], 'forbid': ['micro-behaviors/process/create/shell/git::global-hook-background-helper', 'objectives/persistence/system/git-hooks::decoded-response-global-hook-persistence'], 'hostile_max': 0},
    'response-helper-quoted-source.js': {'require': [], 'forbid': ['micro-behaviors/process/create/local-exec::activation-decoded-response-helper', 'micro-behaviors/process/create/shell/git::global-hook-background-helper', 'objectives/persistence/system/git-hooks::decoded-response-global-hook-persistence'], 'hostile_max': 0},
    'decoded-response-hook-loader.vsix': {'require': ['objectives/persistence/system/git-hooks::decoded-response-global-hook-persistence'], 'hostile_min': 1},
    'nested-language-client/package.json': {'require': ['metadata/package/entrypoint::vscode-analysis-description-without-local-entrypoint'], 'forbid': ['objectives/supply-chain/impersonation/extensions::vscode-analysis-claim-without-code'], 'criticality_max': 3},
    'nested-language-server.vsix': {'require': ['metadata/package/entrypoint::vscode-analysis-description-without-local-entrypoint'], 'forbid': ['objectives/supply-chain/impersonation/extensions::vscode-analysis-claim-without-code'], 'criticality_max': 3},
    'analysis-description-no-entry/package.json': {'require': ['metadata/package/entrypoint::vscode-analysis-description-without-local-entrypoint'], 'forbid': ['objectives/supply-chain/impersonation/extensions::vscode-analysis-claim-without-code'], 'criticality_max': 3},
    'analysis-description-with-entry/package.json': {'forbid': ['metadata/package/entrypoint::vscode-analysis-description-without-local-entrypoint', 'objectives/supply-chain/impersonation/extensions::vscode-analysis-claim-without-code'], 'criticality_max': 3},
    'nonextension-analysis-description/package.json': {'forbid': ['metadata/package/entrypoint::vscode-analysis-description-without-local-entrypoint', 'objectives/supply-chain/impersonation/extensions::vscode-analysis-claim-without-code'], 'criticality_max': 3},
    'socket-process-crypto-library.so': {'require': ['micro-behaviors/communications/socket/connect::library-socket-client', 'micro-behaviors/process/create/fork::fork-shell-operations', 'micro-behaviors/crypto/library/implementation::multiple-crypto-primitive-markers'], 'forbid': ['objectives/supply-chain/trojanized/backdoor::unexpected-capabilities'], 'criticality_max': 3},
}
engine = os.environ.get('CLEAVE', str(REPO.parent / 'cleave/target/release/cleave'))
# Analyze exact fixture bytes outside test-directory guards, as real downloads.
with tempfile.TemporaryDirectory(prefix='vsix-technique-check-', dir='/var/tmp') as work:
    for name in CASES:
        target = Path(work) / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(HERE / name, target)
    result = subprocess.run([engine, '--traits-dir', str(REPO), '--format', 'json', *[str(Path(work) / name) for name in CASES]], capture_output=True, text=True, check=True, timeout=600)
decoder = json.JSONDecoder()
remaining = result.stdout
reports = {}
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    files = report.get('files', [])
    if files:
        reports[Path(files[0]['path']).relative_to(work).as_posix()] = files
errors = []
for name, expected in CASES.items():
    files = reports.get(name)
    if files is None:
        errors.append(f'{name}: missing report')
        continue
    findings = {t['id']: t['crit'] for f in files for t in f.get('traits', [])}
    root = {t['id']: t['crit'] for t in files[0].get('traits', [])}
    high = {k: v for k, v in findings.items() if v >= 4}
    for rule in expected.get('require', []):
        if rule not in findings:
            errors.append(f'{name}: missing {rule}')
    for rule in expected.get('forbid', []):
        if rule in findings:
            errors.append(f'{name}: unexpected {rule}')
    for level, crit in [('hostile', 5), ('suspicious', 4)]:
        count = sum(value >= crit for value in root.values())
        if count < expected.get(level + '_min', 0) or count > expected.get(level + '_max', float('inf')):
            errors.append(f'{name}: {level} count {count}')
    if max(findings.values(), default=0) > expected.get('criticality_max', 5):
        errors.append(f'{name}: unexpected high findings {high}')
    print(f'{name}: {len(high)} suspicious/hostile traits')
assert not errors, '\n'.join(errors)
print(f'PASS: {len(CASES)} cases')
