from pathlib import Path
import json

root=Path('/home/t/src/traits-dev')
def go_call_rule(path,identifier,desc,caller,callee,crit='notable',extra_strings='',extra='true'):
    # Recover Go 1.20+ function identities through pclntab metadata, then
    # verify an actual E8 call inside the caller's function extent. A loose
    # name string or an unused imported routine cannot satisfy this matcher.
    encoded_callee = ('/'+r'[A-Za-z0-9_\x2f.\x2d]{1,160}\.'+callee.rsplit('.',1)[1]+r'\x00/' if callee.startswith('core/') else json.dumps(callee+'\0').replace('\\u0000','\\x00'))
    source='''import "pe"
rule RULE {
  strings:
    $pcln = { F1 FF FF FF 00 00 01 08 }
    $caller = /CALLER\\x00/
    $callee = CALLEE
    EXTRA_STRINGS
  condition:
    pe.is_pe and pe.machine == pe.MACHINE_AMD64 and filesize < 64MB and
    $caller and $callee and $pcln and
    for any h in (1..#pcln) : (
      with hdr = @pcln[h] : (
        uint64(hdr+8) > 0 and uint64(hdr+8) < 100000 and
        with table = hdr+uint64(hdr+64), names = hdr+uint64(hdr+32), text = uint64(hdr+24) : (
          table+uint64(hdr+8)*8+8 < filesize and names < filesize and
          for any i in (0..uint64(hdr+8)-1) : (
            with funcmeta = table+uint32(table+i*8+4) : (
              funcmeta+8 < filesize and
              for any n in (1..#caller) : (
                names+int32(funcmeta+4) <= @caller[n] and
                @caller[n]-(names+int32(funcmeta+4)) < 160 and
                for all z in (names+int32(funcmeta+4)..@caller[n]) : (uint8(z) != 0) and
                with start = text+uint32(table+i*8), extent = uint32(table+(i+1)*8)-uint32(table+i*8) : (
                  extent > 5 and extent < 32768 and
                  with code = pe.rva_to_offset(start-pe.image_base) : (
                    code+extent <= filesize and
                    (EXTRA) and
                    for any j in (0..uint64(hdr+8)-1) : (
                      with destmeta = table+uint32(table+j*8+4) : (
                        destmeta+8 < filesize and
                        for any m in (1..#callee) : (
                          names+int32(destmeta+4) <= @callee[m] and
                          @callee[m]-(names+int32(destmeta+4)) < 160 and
                          for all z in (names+int32(destmeta+4)..@callee[m]) : (uint8(z) != 0) and
                          for any callsite in (code..code+extent-5) : (
                            uint8(callsite) == 0xe8 and
                            start+(callsite-code)+5+int32(callsite+1) == text+uint32(table+j*8)
                          )
                        )
                      )
                    )
                  )
                )
              )
            )
          )
        )
      )
    )
}'''.replace('RULE',identifier.replace('-','_')).replace('CALLER',caller).replace('CALLEE',encoded_callee).replace('EXTRA_STRINGS',extra_strings).replace('EXTRA',extra)
    data='defaults:\n  platforms: [windows]\n  for: [pe, dll]\n  arch: [x86-64]\ntraits:\n  - id: '+identifier+'\n    desc: '+desc+'\n    crit: '+crit+'\n    conf: 0.98\n    if:\n      type: yara\n      source: |\n'+''.join('        '+l+'\n' for l in source.splitlines())
    p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(data)

prefix=r'[A-Za-z0-9_\x2f.\x2d]{1,160}'
go_call_rule('micro-behaviors/process/create/command-handler/go-native-handler-call.yaml',
 'go-script-handler-command-context-call','Go script handler constructs child command',
 prefix+r'\.(executeScript|runCommand|handleCommand|execCommand)', 'os/exec.CommandContext')
go_call_rule('micro-behaviors/os/registry/manipulate/go-native-persistence-call.yaml',
 'go-persistence-registry-value-write-call','Go persistence routine calls registry writer',
 prefix+r'\/persistence\.(Setup|Install|Persist)', 'golang.org/x/sys/windows/registry.Key.setStringValue')
go_call_rule('objectives/anti-analysis/debugger-detect/combined-checks/go-native-check-call.yaml',
 'go-check-driver-calls-antidebug','Go check dispatcher calls anti-debug routine',
 prefix+r'\.(RunChecks|runChecks)', 'core/cmd/agent/protect.antiDebug', 'suspicious')
go_call_rule('objectives/anti-analysis/environment-detect/check/go-native-check-call.yaml',
 'go-check-driver-calls-antivm','Go check dispatcher calls anti-VM routine',
 prefix+r'\.(RunChecks|runChecks)', 'core/cmd/agent/protect.antiVM', 'suspicious')
# The ROOT literal is tied to an in-function RIP-relative address, the
# four-byte Go string length and the UTF16 conversion call. Certificate
# packet constants and two API error names are restricted to the same routine.
extra='''for any r in (code..code+extent-16) : (
  uint32(r) & 0xffffff == 0x058d48 and uint8(r+7) == 0xbb and uint32(r+8) == 4 and
  uint8(r+12) == 0xe8 and
  uint32(pe.rva_to_offset(start+(r-code)+7+int32(r+3)-pe.image_base)) == 0x544f4f52
) and
for any k in (1..#asn) : (@asn[k] >= code and @asn[k] < code+extent)'''
go_call_rule('micro-behaviors/crypto/certificate/install/go-native-root.yaml',
 'go-root-certificate-request-routine','Go ROOT certificate-install request routine',
 prefix+r'\.(installCertToStore|installCertificateToStore)',
 'golang.org/x/sys/windows.(*LazyProc).Call','suspicious',
 '$asn = { 48 C7 40 08 01 00 01 00 [0-40] 48 C7 40 20 03 00 00 00 }', extra)
