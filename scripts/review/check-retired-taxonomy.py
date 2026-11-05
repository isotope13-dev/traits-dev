#!/usr/bin/env python3
"""Reject retired non-process taxonomy branches and their live references."""
import argparse
import re
from pathlib import Path

RETIRED = {
    'metadata/file/invisible-unicode':
        'Use the character property, source or binary evidence, or named product subject.',
    'metadata/file/comment':
        'Use the source-comment, document-markup, behavior, or objective subject.',
    'metadata/file/naming':
        'Use source identifier populations, function naming, or the specific literal subject.',
    'metadata/file/import':
        'Use metadata/import/count for import counts or the named dependency subject.',
    'metadata/file/attribution':
        'Use source attribution, license, or the specific named provenance subject.',
    'metadata/file/system-info':
        'Use the system-information or privilege subject evidenced by the observation.',
    'metadata/file/system-info/privilege-name':
        'Use privilege reference evidence; a name alone does not establish privilege use.',
    'micro-behaviors/communications/url/http-path':
        'Use the observed URL resource, request, construction, or named-service subject.',
    'micro-behaviors/communications/url/http-path/service':
        'Use the named service, protocol, or observed endpoint subject.',
    'micro-behaviors/communications/url/http-path/bot':
        'Use the automation endpoint or named service subject.',
    'micro-behaviors/communications/url/http-path/resource':
        'Use the resource, request, URL construction, or named-product subject.',
    'objectives/command-and-control/backdoor/dispatch/legacy':
        'Use the named program or the observed command-and-control behavior.',
    'metadata/file/profile':
        'Use the most likely behavior or objective, or the actual neutral evidence subject.',
    'metadata/file/profile/script/transformation':
        'Use the observed transformation, execution behavior, or supported objective.',
    'metadata/file/profile/script/evaluation':
        'Use the observed evaluation, process, code construction, or supported objective.',
    'metadata/file/profile/script/network':
        'Use the observed network, interpreter execution, or supported objective.',
    'metadata/file/profile/script/automation':
        'Use the named library, observed automation, interpreter, or neutral syntax subject.',
    'metadata/file/profile/process':
        'Use the observed process behavior, command, or supported objective.',
    'metadata/file/profile/process/shell':
        'Use the observed shell operation, argument, interpreter input, or supported objective.',
    'metadata/file/profile/process/creation-api':
        'Use the observed process creation, API reference, command, or supported objective.',
    'metadata/file/profile/process/evaluation':
        'Use the observed interpreter, evaluation, process, network, or supported objective.',
    'metadata/file/profile/process/hidden':
        'Use process launch, window configuration, argument syntax, or the supported objective.',
    'metadata/file/profile/process/artifact':
        'Use the observed execution, injection, file, cryptographic, or diagnostic subject.',
    'metadata/file/profile/windows-api':
        'Use the supported behavior or objective reflected by the API combination.',
    'metadata/file/profile/memory':
        'Use the observed memory, process, file, or supported execution subject.',
    'metadata/file/profile/memory/protection-code':
        'Use memory protection, allocation, network, instruction, or supported execution evidence.',
    'metadata/file/profile/memory/protection-context':
        'Use the observed memory operation, API resolution, or supported subject.',
    'metadata/file/profile/memory/protection-api':
        'Use the observed memory operation, API resolution, or language class reference.',
    'metadata/file/profile/pe-loader-context':
        'Use the observed executable property or supported loading, injection, or evasion behavior.',
    'metadata/file/profile/pe-loader-context/resource':
        'Use resource access, named components, or the supported staging, packing, or evasion objective.',
    'metadata/file/profile/pe-loader-context/layout':
        'Use the measured binary property or supported loading, packing, or evasion behavior.',
    'metadata/file/profile/pe-loader-context/network':
        'Use the observed network behavior, named packer, or supported execution objective.',
    'metadata/file/profile/pe-loader-context/resolution':
        'Use the observed API-resolution behavior or supported obfuscation objective.',
    'metadata/file/profile/com':
        'Use the named COM component or its supported operation or objective.',
    'metadata/file/profile/com/encoded':
        'Use the named component or the supported encoding and obfuscation behavior.',
    'metadata/file/profile/com/progid':
        'Use the named COM component or the supported operation.',
    'metadata/file/profile/com/class-id':
        'Use the named COM component or the supported object-creation behavior.',
    'metadata/file/profile/com/interface':
        'Use the named component, COM interface, or supported operation.',
    'metadata/file/profile/com/registration':
        'Use COM registration or the supported registry, persistence, or execution subject.',
    'metadata/file/profile/text-shape':
        'Use the observed subject, supported behavior, or specific neutral text property.',
    'metadata/file/profile/string-population':
        'Use the observed string property, subject, supported behavior, or objective.',
    'metadata/file/profile/co-occurrence':
        'Use the supported behavior or objective, describing co-occurrence precisely.',
    'metadata/file/profile/tool-reference':
        'Use the named tool or the specific observed behavior and evidence.',
    'metadata/file/profile/module-loading':
        'Use the supported module loading, resource access, reflection, or execution objective.',
    'metadata/file/profile/command-options':
        'Use the specific command argument, process behavior, or named tool.',
    'metadata/file/profile/firmware':
        'Use firmware format evidence, binary section bytes, or the supported operation.',
    'metadata/file/profile/execution-api':
        'Use process creation, replacement, interpreter, or the supported execution objective.',
    'metadata/file/profile/operation-reference':
        'Use the specific execution, transfer, application hook or file behavior.',
    'metadata/file/profile/command-reference':
        'Use the specific command behavior, named tool, or neutral argument and literal evidence.',
    'metadata/file/profile/shell-execution':
        'Use the supported shell, process, command-dispatch or execution objective.',
    'metadata/file/profile/socket-api':
        'Use connection, socket operation, port scanning, or supported shell-control behavior.',
    'metadata/file/profile/socket-runtime':
        'Use socket connection, initialization, syscall or API-resolution behavior.',
    'metadata/file/profile/module-interop':
        'Use the specific service, reflection, process, or network behavior.',
    'metadata/file/profile/eval-reference':
        'Use the specific code evaluation, decoding, or serialization behavior.',
    'metadata/file/profile/mcp':
        'Use MCP communications, the specific supporting behavior, or the named tool.',
    'metadata/file/profile/tool-interface':
        'Use the specific tool dispatch, operation, or source naming subject.',
    'metadata/file/profile/jvm-constants':
        'Use the specific JVM behavior or neutral constant evidence.',
    'metadata/file/profile/identity':
        'Use the specific file format, installer evidence or named product.',
    'metadata/file/profile/lua-runtime':
        'Use the specific Lua reflection, source layout or obfuscation behavior.',
    'metadata/file/profile/resource-reference':
        'Use the specific resource path or named vendor component.',
    'metadata/file/profile/architecture-reference':
        'Use architecture naming or supported architecture behavior.',
    'metadata/file/profile/audit-verdict':
        'Use the specific security assessment evidence.',
    'metadata/file/profile/emoji-reference':
        'Use the specific Unicode or text-processing evidence.',
    'metadata/file/profile/rtf-object':
        'Use the specific object behavior, obfuscation or document evidence.',
    'metadata/file/profile/ole-link':
        'Use linked-object, URL or remote-resource evidence.',
    'metadata/file/profile/libc':
        'Use runtime references, binary symbols or runtime filename evidence.',
    'metadata/file/profile/file-operation':
        'Use the specific file operation or data transformation.',
    'metadata/file/profile/system-management':
        'Use the specific system behavior, path, tool, or supported objective.',
    'metadata/file/profile/task-command':
        'Use the specific command behavior, task configuration or execution trigger.',
    'metadata/file/profile/url-construction':
        'Use URL construction, HTTP behavior or the supported objective.',
    'metadata/file/profile/tls':
        'Use TLS initialization, verification or the supported objective.',
    'metadata/file/profile/key-recovery':
        'Use key-recovery behavior or the specific mathematical vocabulary.',
    'metadata/file/profile/patch-context':
        'Use the observed patch content or supported execution objective.',
    'metadata/file/profile/container':
        'Use the specific container interface or observed behavior.',
    'metadata/file/profile/error-reporting':
        'Use the specific diagnostic wording or error behavior.',
    'metadata/file/profile/license-reference':
        'Use license declarations or license-validation behavior.',
    'metadata/file/profile/upstream-attribution':
        'Use the specific source attribution or license evidence.',
    'metadata/file/profile/relay-framing':
        'Use relay behavior, stream framing or the specific data schema.',
    'metadata/file/profile/registry':
        'Use the specific registry behavior, source name or supported objective.',
    'metadata/file/profile/upload-config':
        'Use copy-destination or upload configuration evidence.',
    'metadata/file/profile/input-context':
        'Use the supported input-capture objective or observed input behavior.',
    'metadata/file/profile/finance':
        'Use financial names, injection behavior or the supported objective.',
    'metadata/file/profile/telemetry-identity':
        'Use telemetry behavior and the specific identity evidence.',
    'metadata/file/profile/version-comment':
        'Use the relevant executable version field.',
    'metadata/file/profile/office-embedded':
        'Use the embedded document structure or supported execution objective.',
    'metadata/file/profile/proxy-implementation':
        'Use the named proxy library, proxy behavior, or specific objective.',
    'metadata/file/profile/log-reference':
        'Use the specific log path or observed logging behavior.',
    'metadata/file/profile/scanner':
        'Use the specific security scanning behavior, objective, or artifact.',
    'metadata/file/profile/scanner/indications':
        'Use the specific scanning behavior or communication subject.',
    'metadata/file/profile/scanner/evidence':
        'Use security scanning evidence or the concrete manifest format.',
    'metadata/file/profile/scanner/vulnerability':
        'Use vulnerability scanning or the specific evidence subject.',
    'metadata/file/profile/scanner/security':
        'Use the specific security scanning evidence or behavior.',
    'metadata/file/profile/secret-scanning':
        'Use credential auditing or secret redaction behavior.',
    'metadata/file/profile/web-scanning':
        'Use web security auditing behavior or the named scanner.',
    'metadata/file/profile/transfer/http-download':
        'Use the supported download behavior, execution objective or named service.',
    'metadata/file/profile/attack-config-schema':
        'Use the specific schema and supported objective.',
    'metadata/file/profile/wallet-rpc':
        'Use wallet RPC method evidence or the supported obfuscation objective.',
    'metadata/file/profile/window-api':
        'Use window control, station, or process configuration evidence.',
    'metadata/file/profile/android-asset-context':
        'Use asset loading, staged execution, archive packing, or the observed file operation.',
    'metadata/file/profile/security':
        'Use the supported defensive behavior, security evasion, or specific evidence.',
    'metadata/file/profile/security/policy':
        'Use defensive policy, risk assessment, or supported log removal.',
    'metadata/file/profile/security/hunting':
        'Use security scanning evidence or the supported activity.',
    'metadata/file/profile/lexical/installer-methods':
        'Use the specific installation, transfer, extraction, or system operation.',
    'metadata/file/profile/lexical/string-join':
        'Use the specific string-joining behavior.',
    'metadata/file/profile/lexical/operator-population':
        'Use arithmetic or bitwise observations and supported objectives.',
    'metadata/file/profile/mobile-config':
        'Use mobile build configuration, permissions, bundle observations, or the named product.',
    'metadata/file/profile/rpc':
        'Use RPC communication, the specific operation, or named product evidence.',
    'metadata/file/profile/temp-path':
        'Use temporary artifact paths or the supported operation.',
    'metadata/file/profile/macro':
        'Use macro execution, document behavior, or the specific supported operation.',
    'metadata/file/profile/document/parsing':
        'Use the specific document parsing or extraction behavior.',
    'metadata/file/profile/document':
        'Use document operations, format evidence, or the named product.',
    'metadata/file/profile/decryption':
        'Use the cipher, decryption operation, or supported execution or credential objective.',
    'metadata/file/profile/environment':
        'Use environment access, CI context, or the supported operation.',
    'metadata/file/profile/pe-api':
        'Use the specific API behavior or supported execution and obfuscation objective.',
    'metadata/file/profile/crypto-envelope':
        'Use the specific cryptographic operation, format, or named library.',
    'metadata/file/profile/mobile-api':
        'Use platform references, named tools, or the specific mobile behavior.',
    'metadata/file/profile/product-reference':
        'Use named products, provenance observations, or the supported behavior.',
    'metadata/file/profile/agent/session':
        'Use agent session records, named tools, or the specific behavior.',
    'metadata/file/profile/agent/instruction':
        'Use the specific agent instruction or supported objective.',
    'metadata/file/profile/agent':
        'Use agent behavior, configuration, session evidence, or the named tool.',
    'metadata/file/profile/library/build':
        'Use compiler metadata or the supported build operation.',
    'metadata/file/profile/library/compression':
        'Use the specific compression evidence.',
    'metadata/file/profile/library/event-loop':
        'Use event-loop behavior or the named library.',
    'metadata/file/profile/library/module-name':
        'Use library paths, module-name references, or supported resolution behavior.',
    'metadata/file/profile/library/debugging':
        'Use debugger and process-control references.',
    'metadata/file/profile/library/graphics':
        'Use display, graphics, window, image, or IPC behavior.',
    'metadata/file/profile/graphics/capture':
        'Use display capture references or the evidenced capture behavior.',
    'metadata/file/profile/graphics/representation':
        'Use the evidenced image representation or operation.',
    'metadata/file/profile/graphics/reference':
        'Use display, dynamic linking, image, or embedded-payload evidence.',
    'metadata/file/profile/graphics/co-occurrence':
        'Use the evidenced graphics behavior or likely objective.',
    'metadata/file/profile/graphics':
        'Use the evidenced graphics behavior or likely objective.',
    'metadata/file/profile/cryptography':
        'Use the likely cryptographic operation or generic value evidence.',
    'metadata/file/profile/token-shape':
        'Use the evidenced encoding, padding, or credential subject.',
    'metadata/file/profile/unicode-text':
        'Use Unicode processing, concatenation, or neutral text shape.',
    'metadata/file/profile/transfer/http-exchange':
        'Use Git operations or the specific encoded value.',
    'metadata/file/profile/transfer':
        'Use the specific transfer behavior or objective.',
    'metadata/file/profile/operation-cooccurrence':
        'Use the supported operation, objective, or neutral text subject.',
    'metadata/file/profile/field-presence':
        'Use the evidenced operation, objective, or field subject.',
    'metadata/file/profile/syntax-tree':
        'Use source measurements, array representation, or dynamic execution.',
    'metadata/file/profile/token-population':
        'Use the specific text distribution, subject, or behavior.',
    'metadata/file/profile/com/shortcut':
        'Use shortcut configuration, generic method behavior, or COM interface evidence.',
    'metadata/file/profile/co-occurrence/instruction':
        'Use the evidenced buffer, arithmetic, bitwise, or instruction observation.',
    'metadata/file/profile/co-occurrence/bitwise':
        'Use the specific bitwise operation and its data flow.',
    'metadata/file/profile/host-information':
        'Use the observed host, build, or execution subject.',
    'metadata/file/profile/structured':
        'Use the specific structured observation or behavior.',
    'metadata/file/profile/encoding/composition':
        'Use the encoded carrier or specific documentation and vocabulary evidence.',
    'metadata/file/profile/encoding/compression':
        'Use compression behavior, destination paths, or literal evidence.',
    'metadata/file/profile/installer/msi/properties':
        'Use installer launch, maintenance, product, or package evidence.',
    'metadata/file/profile/installer/msi/layout':
        'Use installer layout or the identified packaging product.',
    'metadata/file/profile/installer/msi/libraries':
        'Use the named library or package string evidence.',
    'metadata/file/profile/process/injection':
        'Use injection behavior, type syntax, or neutral text fragments.',
    'metadata/file/profile/process/launch':
        'Use process arguments or executable path evidence.',
    'metadata/file/profile/script/timing':
        'Use the evidenced timing or string-obfuscation behavior.',
    'metadata/file/profile/tunnel':
        'Use the specific tunnel, forwarding, named tool, or persistence behavior.',
    'metadata/file/profile/pe-loader-context/php-endpoint':
        'Use the observed HTTP client or supported execution behavior.',
    'metadata/file/profile/tunnel/setup':
        'Use named tunnel tools, forwarding, or service persistence evidence.',
    'metadata/file/profile/tunnel/implementation':
        'Use the specific tunnel, forwarding, proxy, or named library evidence.',
    'metadata/file/profile/tunnel/reference':
        'Use named tunnel tools or the observed forwarding behavior.',
    'metadata/file/profile/tunnel/provider':
        'Use named providers or the specific authentication and endpoint behavior.',
    'metadata/file/profile/network-context':
        'Use the evidenced communication, process, execution, or named subject.',
    'metadata/file/profile/malware-reference':
        'Use the named malware family or a neutral description of generic evidence.',
    'metadata/file/profile/blockchain':
        'Use the evidenced blockchain operation, protocol, named service, or supported objective.',
    'metadata/file/profile/embedded-binary':
        'Use the evidenced binary structure, embedded payload, named product, or supported objective.',
    'metadata/file/profile/credential-terms':
        'Use the evidenced credential source, operation, vocabulary, named product, or supported objective.',
    'metadata/file/profile/path-reference':
        'Use the evidenced filesystem or URL subject, operation, named product, or supported objective.',
    'metadata/file/profile/markup':
        'Use the evidenced document format, markup operation, named product, or supported objective.',
    'metadata/file/profile/encoding':
        'Use the evidenced codec, operation, format, literal, or supported objective.',
    'metadata/file/profile/browser':
        'Use the evidenced browser operation, collection, exfiltration, or named application subject.',
    'metadata/file/profile/browser/state':
        'Use the evidenced browser storage, cookie access, exfiltration, or named application subject.',
    'metadata/file/profile/network-context/storage':
        'Use the storage URL, web-storage write, or file-sync behavior.',
    'metadata/file/profile/network-context/dns':
        'Use DNS query behavior or the supported control, execution, or exfiltration objective.',
    'metadata/file/profile/network-context/code-forge':
        'Use named services or the observed URL and release reference.',
    'metadata/file/profile/network-context/credential':
        'Use the evidenced credential access, collection, or cloud operation.',
    'metadata/file/profile/network-context/native':
        'Use the evidenced network request or binary observation.',
    'metadata/file/profile/network-context/cdn':
        'Use named providers or package asset evidence.',
    'metadata/file/profile/installer/machine-learning':
        'Use observed vocabulary, named libraries, or Python execution behavior.',
    'metadata/file/profile/installer/configuration':
        'Use installer hooks, install behavior, or the evidenced packing.',
    'metadata/file/profile/installer/product/catalog':
        'Use metadata/installer/product for the reviewed installer-product selector.',
    'metadata/file/profile/installer/properties':
        'Use named installer evidence or the observed privilege behavior.',
    'metadata/file/profile/installer/bundle':
        'Use the named packaging tool or evidenced installer behavior.',
    'metadata/file/profile/installer/structure':
        'Use the evidenced packaging tool, configuration, file, or resource subject.',
    'metadata/file/profile/installer/product/archive':
        'Use the named self-extractor, extraction behavior, or evidenced archive subject.',
    'metadata/file/profile/installer/product':
        'Use the named product or evidenced installation, packaging, or extraction behavior.',
    'metadata/file/profile/network-context/encoded':
        'Use the evidenced encoding, communication, or payload subject.',
    'metadata/file/profile/network-context/activity':
        'Use the evidenced communication, process, collection, or execution subject.',
    'metadata/file/profile/network-context/endpoint':
        'Use the evidenced URL, header, service, communication, or objective subject.',
    'metadata/file/profile/network-context/host':
        'Use the evidenced communication, host discovery, exfiltration, or execution subject.',
    'metadata/file/profile/network-context/process':
        'Use the evidenced communication, process, execution, exfiltration, or named tool subject.',
    'metadata/file/profile/installer/lifecycle':
        'Use the evidenced installation, execution, persistence, or product subject.',
    'metadata/file/profile/installer/plugin':
        'Use installer recognition, named DLL evidence, or the supported packing and execution objective.',
    'metadata/file/profile/installer/resource':
        'Use the evidenced packing, resource extraction, or file entropy.',
    'metadata/file/profile/installer/branding':
        'Use the evidenced obfuscation or named product.',
    'metadata/file/profile/installer/encoding':
        'Use the evidenced encoding or script behavior.',
    'metadata/file/profile/installer':
        'Use the evidenced installation, behavior, objective, product, or property.',
    'metadata/file/profile/shortcut/construction':
        'Use shortcut creation, command paths, or the evidenced download behavior.',
    'metadata/file/profile/shortcut/encoding':
        'Use the evidenced decoding, decompression, encoded content, or marker subject.',
    'metadata/file/profile/shortcut/extension':
        'Use the evidenced argument, target path, or extension masquerade.',
    'metadata/file/profile/shortcut/path':
        'Use the evidenced executable, path, network share, or masquerade subject.',
    'metadata/file/profile/shortcut/script-and-command':
        'Use the evidenced interpreter, process, file, network, or execution subject.',
    'metadata/file/profile/shortcut/options':
        'Use the specific command option, interpreter, or error-suppression behavior.',
    'metadata/file/profile/shortcut/com-automation':
        'Use the specific COM automation, HTTP, or stream behavior.',
    'metadata/file/profile/shortcut':
        'Classify shortcut evidence by its observed behavior, objective, or property.',
    'metadata/file/profile/binary-strings':
        'Use the observed text subject, behavior, or named product.',
    'metadata/file/profile/text-distribution':
        'Use text distributions, line shape, padding, entropy, or behavior.',
    'metadata/file/profile/function-population':
        'Use function measurements, declaration names, or the supported behavior.',
    'metadata/file/profile/identifier-population':
        'Use identifier naming, declarations, or the supported behavior.',
    'metadata/file/profile/archive':
        'Use archive structure, operations, or the supported objective.',
    'metadata/file/profile/test-indications':
        'Use the specific test, fixture, or path evidence.',
    'metadata/file/profile/source-indications':
        'Use the specific source subject, behavior, or objective.',
    'metadata/file/profile/overlay':
        'Use overlay structure, payload evidence, packing, or the supported objective.',
    'metadata/file/profile/library/runtime':
        'Use the evidenced interpreter, linker, plugin, or named product.',
    'metadata/file/profile/library':
        'Use the evidenced behavior, library reference, or named product.',
    'metadata/file/profile/lexical/managed-method-names':
        'Use the behavior suggested by the method name.',
    'metadata/file/profile/relay-implementation':
        'Use the evidenced function name or relay behavior.',
    'metadata/file/profile/user-agent':
        'Use the evidenced download or HTTP behavior.',
    'metadata/file/profile/visibility':
        'Use the specific literal or visibility behavior.',
    'metadata/file/profile/package-provenance':
        'Use the evidenced supply-chain objective or actual provenance.',
    'metadata/file/profile/mobile-collection':
        'Use the specific mobile input or communication behavior.',
    'metadata/file/profile/prompt-example':
        'Use the specific dialog or prompt evidence.',
    'metadata/file/profile/transfer/http-upload/reference':
        'Use file-upload guidance and its supported behavior.',
    'metadata/file/profile/transfer/http-upload/command':
        'Use the supported upload behavior or named service.',
    'metadata/file/profile/transfer/cloud':
        'Use the named cloud product or the supported transfer objective.',
    'metadata/file/profile/staging':
        'Use the supported execution, collection, process or path subject.',
    'metadata/file/profile/transfer/upload-api':
        'Use HTTP request or upload behavior and distinguish symbol references from calls.',
    'metadata/file/profile/memory/fiber':
        'Use fiber behavior and distinguish memory co-occurrence from a bound callback.',
    'metadata/file/profile/executable-config':
        'Use process configuration, temporary-path, or specific supported behavior.',
    'metadata/file/profile/open-handler':
        'Use OS handler dispatch or the specific supported process operation.',
    'metadata/file/profile/locale':
        'Use locale processing, country-selection or UI localization evidence.',
    'metadata/file/profile/screen-capture':
        'Use capture or monitoring behavior, or the named library.',
    'metadata/file/profile/screen-capture/references':
        'Use capture, display, UI or named-library evidence.',
    'metadata/file/profile/screen-capture/cooccurrence':
        'Use screenshot behavior, monitoring or multi-source collection.',
    'metadata/file/profile/process/network':
        'Use staged execution, scheduling or the observed process operation.',
    'metadata/file/profile/process/stdio':
        'Use process standard-I/O operations or interpreter-input behavior.',
    'metadata/file/profile/process/termination':
        'Use process termination behavior or the likely collection or evasion objective.',
    'metadata/file/profile/payload-building':
        'Use source-generation behavior for payload-building clues.',
    'metadata/file/profile/payment-request':
        'Use payment-related HTTP and form behavior.',
    'metadata/file/profile/media-projection':
        'Use Android display projection and virtual-display behavior.',
    'metadata/file/profile/gpu-api':
        'Use GPU management behavior or NVIDIA library identity.',
    'metadata/file/profile/android-native':
        'Use Android native staging or DEX loader behavior.',
    'metadata/file/profile/socks-protocol':
        'Use SOCKS protocol, server, relay or reverse-proxy behavior.',
    'metadata/file/profile/automation-management':
        'Use the named application or the supported automation behavior.',
    'metadata/file/profile/cron':
        'Use the supported cron operation or persistence objective.',
    'metadata/file/profile/encoding/serialization':
        'Use the supported parsing or serialization behavior.',
    'metadata/file/profile/file-operation/write-api':
        'Use the supported filesystem read or write behavior.',
    'micro-behaviors/fs/read/file/full':
        'Use file content reads; not every observation establishes a complete read.',
    'metadata/file/profile/file-operation/deletion':
        'Use the supported filesystem deletion behavior.',
    'metadata/file/profile/file-operation/read':
        'Use the supported filesystem read or enumeration behavior.',
    'metadata/file/profile/registry/messaging':
        'Use the registry software target or supported collection behavior.',
    'metadata/file/profile/registry/execution':
        'Use the supported process-hijack or impact objective.',
    'metadata/file/profile/registry/configuration':
        'Use the supported session-manager, service or policy behavior.',
    'metadata/file/profile/registry/association':
        'Use registry association operations or the supported bypass objective.',
    'metadata/file/profile/agent/management':
        'Use the likely agent operation or supported supply-chain objective.',
    'metadata/file/profile/randomness':
        'Use random generation or the supported timing behavior.',
    'metadata/file/profile/xor':
        'Use the supported XOR operation.',
    'metadata/file/profile/editor':
        'Use the named editor library or the likely interpreter behavior.',
    'metadata/file/profile/timezone':
        'Use locale timezone metadata or the supported behavior.',
    'metadata/file/profile/smb-protocol':
        'Use SMB communication behavior and protocol components.',
    'metadata/file/profile/shell-token':
        'Use shell interpreter evidence.',
    'metadata/file/profile/data-dispatch':
        'Use the likely evaluation, callback or dispatch behavior.',
    'metadata/file/profile/data-retrieval':
        'Use the likely retrieval, decoding or staging behavior.',
    'metadata/file/profile/alphabet':
        'Use character-set alphabet metadata or the supported operation.',
    'metadata/file/profile/user-input':
        'Use input monitoring or the supported collection objective.',
    'metadata/file/profile/console-api':
        'Use console input or output behavior.',
    'metadata/file/profile/secret-storage':
        'Use the supported credential-access objective.',
    'metadata/file/profile/windows-input-capture':
        'Use the supported multi-source collection objective.',
    'metadata/file/profile/clipboard-process':
        'Use the clipboard monitoring behavior.',
    'metadata/file/profile/office-addin':
        'Use the likely plugin execution trigger.',
    'metadata/file/profile/industrial-control':
        'Use industrial vocabulary or the supported behavior.',
    'metadata/file/profile/http-response':
        'Use the likely remote-command behavior or objective.',
    'metadata/file/profile/download-execution':
        'Use the likely acquisition, execution, package trigger or Git operation.',
    'metadata/file/profile/installer/layout':
        'Use installer metadata by subject or the supported behavior.',
    'metadata/build/toolchain':
        'Use the compiler, build configuration, tool name or observed operation.',
    'micro-behaviors/os/env/enumeration':
        'Use environment enumeration.',
    'micro-behaviors/os/env/dump':
        'Use environment enumeration or the supported collection objective.',
    'micro-behaviors/os/env/modify':
        'Use environment writes.',
    'micro-behaviors/os/env/check':
        'Use environment tests.',
    'micro-behaviors/os/env/gate':
        'Use environment tests or supported conditional behavior.',
    'micro-behaviors/os/env/user-paths':
        'Use environment paths or the observed path subject.',
    'micro-behaviors/os/service/driver':
        'Use kernel driver operations.',
    'micro-behaviors/dylib/library':
        'Use the library identity, capability, or observed symbol.',
    'micro-behaviors/ui/framework':
        'Use the framework identity or supported UI capability.',
    'objectives/collection/email-harvest':
        'Use email collection.',
    'objectives/credential-access/windows-registry':
        'Use registry credential access.',
    'objectives/lateral-movement/social-engineering/spam':
        'Use spam impact.',
    'objectives/lateral-movement/delivery':
        'Use the remote operation or supported objective.',
    'objectives/exfiltration/stealer/network-config':
        'Use system-information network theft.',
    'objectives/exfiltration/stealer/process-list':
        'Use system-information process theft.',
    'objectives/exfiltration/stealer/surveillance':
        'Classify by the stolen item or supported observation.',
    'objectives/exfiltration/stealer/phish':
        'Classify by the stolen item or acquisition behavior.',
    'objectives/supply-chain/install-hook':
        'Classify by supported execution or other objective.',
    'objectives/supply-chain/recon-exfil':
        'Classify discovery or export by supported result.',
    'objectives/supply-chain/credential-theft':
        'Classify credential acquisition or export by source.',
    'objectives/supply-chain/metadata-anomaly':
        'Classify package metadata, destructive behavior, or masquerade.',
    'objectives/anti-static/obfuscation/binary-metrics':
        'Use binary measurements or supported concealment.',
    'objectives/anti-static/obfuscation/code-metrics':
        'Use code measurements or supported concealment.',
    'objectives/anti-static/obfuscation/tools':
        'Use known tools or supported concealment.',
    'objectives/anti-static/obfuscation/multi-layer':
        'Use named concealment or representation observations.',
    'metadata/file/string':
        'Classify each string by its observed subject.',
    'metadata/file/literal':
        'Classify each literal by its type or observed subject.',
    'metadata/file/function':
        'Use function naming, declaration, population, or binary anatomy.',
    'metadata/file/arithmetic':
        'Use arithmetic operations or measured syntax properties.',
    'metadata/hardening/missing':
        'Use the mitigation subject or verified linking facts.',
    'metadata/binary/installer':
        'Use installer identity or the supported binary property.',
    'metadata/binary/framework':
        'Use framework identity or the supported capability.',
    'metadata/binary/vendor':
        'Use vendor observations or verified signatures.',
    'metadata/binary/signing':
        'Use signing or verified signature subjects.',
    'metadata/binary/license':
        'Use license observations by subject.',
    'metadata/binary/toolchain':
        'Use known toolchain or compiler observations.',
    'objectives/credential-access/theft/authentication':
        'Classify authentication evidence by credential source, acquisition, or supporting observation.',
    'metadata/file/encoded':
        'Use file encoding observations.',
    'metadata/lang/encoded':
        'Use language encoding observations.',
    'micro-behaviors/data/db/sql':
        'Classify database operations or SQL syntax by their subject.',
    'objectives/exfiltration/serialization':
        'Use credential export or data serialization by supported behavior.',
    'micro-behaviors/os/network':
        'Classify network operations under network or communications.',
    'micro-behaviors/communications/ipc/irc':
        'Classify IRC operations under communications/irc.',
    'micro-behaviors/crypto/library':
        'Classify by crypto operation, primitive, provider, or observed name.',
    'micro-behaviors/crypto/native':
        'Use crypto provider or the supported operation.',
    'micro-behaviors/crypto/asymmetric/key':
        'Use crypto key operations or representation.',
    'micro-behaviors/crypto/asymmetric/ecdh':
        'Use crypto key exchange.',
    'micro-behaviors/data/source':
        'Classify source syntax, control flow, or metaprogramming by subject.',
    'micro-behaviors/data/encoded':
        'Use encoding observations or decoding operations.',
    'micro-behaviors/fs/shell-ops':
        'Use the supported file operation, UI, or shell namespace.',
    'micro-behaviors/fs/traversal':
        'Use directory traversal or the evidenced filesystem operation.',
    'micro-behaviors/fs/directory/mkdir':
        'Use directory creation.',
    'micro-behaviors/mem/decompress':
        'Use data decompression by algorithm.',
    'micro-behaviors/process/threading':
        'Use thread, synchronization, work, or IPC operations.',
    'micro-behaviors/process/fork':
        'Use process creation by fork.',
    'micro-behaviors/process/user':
        'Use process identity or user administration.',
    'micro-behaviors/process/interpreter/reflection':
        'Use metaprogramming reflection.',
    'micro-behaviors/process/script':
        'Use the observed interpreter or execution mechanism.',
    'micro-behaviors/os/registry/manipulate':
        'Classify registry operations or their supported objective.',
    'objectives/command-and-control/dropper':
        'Classify payload execution, staging, or communication by outcome.',
    'objectives/exfiltration/sensitive-data':
        'Classify collection, credential acquisition, or export by evidence.',
    'metadata/lang/source/literal/value':
        'Classify literals by type, subject, or known identity.',
    'metadata/file/data-blob':
        'Classify the observed binary or text property.',
    'metadata/file/policy':
        'Classify policy evidence by subject.',
    'metadata/package/tooling':
        'Classify build, package, or known-tool evidence.',
    'well-known/malware/supply-chain':
        'Classify known malware by its defining role.',
}
REFERENCE = re.compile(r"^\s*(?:-\s*)?id:\s*['\"]?([^\s'\"#]+)")


def violations(root):
    for retired, guidance in RETIRED.items():
        branch = root / retired
        if branch.is_dir() and any(p.is_file() and p.suffix in ('.yaml', '.yml') for p in branch.rglob('*')):
            yield f'{retired}: retired taxonomy branch; {guidance}'
    for tier in ('metadata', 'micro-behaviors', 'objectives', 'well-known'):
        base = root / tier
        if not base.is_dir():
            continue
        for path in base.rglob('*'):
            if not path.is_file() or path.suffix not in ('.yaml', '.yml'):
                continue
            for number, line in enumerate(path.read_text().splitlines(), 1):
                match = REFERENCE.match(line)
                if not match:
                    continue
                reference = match.group(1).split('::', 1)[0].rstrip('/')
                for retired in RETIRED:
                    if reference == retired or reference.startswith(retired + '/'):
                        yield f'{path.relative_to(root)}:{number}: retired taxonomy reference {match.group(1)}'
                        break


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--traits-dir', type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    errors = list(violations(args.traits_dir))
    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    count = len(RETIRED)
    branch = 'branch' if count == 1 else 'branches'
    print(f'Legacy taxonomy: {count} retired {branch} and live references absent.')


if __name__ == '__main__':
    main()
