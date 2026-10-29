from pathlib import Path
src=Path(__file__).parent;root=Path('/home/t/src/cleave');dst=root/'src/extractors/pyarmor.rs';dst.write_text((src/'pyarmor.rs').read_text())
p=root/'src/extractors/mod.rs';s=p.read_text();line='pub(crate) mod pyarmor;\n'
if line not in s:s=s.replace('pub(crate) mod ps_to_exe;\n','pub(crate) mod ps_to_exe;\n'+line);p.write_text(s)
p=root/'src/analyzers/archive/analyzers.rs';s=p.read_text();needle='        // Find the SHA-256 of the bundled Python shared library, if present.'
assert s.count(needle)==1
if 'Static PyArmor recovery' not in s:
 s=s.replace(needle,'''        // Static PyArmor recovery requires its companion runtime. Preserve
        // original members and attach decoded bytecode as a separate child;
        // encrypted format identity itself supplies no hostile classification.
        let mut decoded = Vec::new();
        for member in &members {
            if !member.data.windows(8).any(|v| v == b"PY000000") { continue; }
            for runtime in &members {
                if !runtime.data.windows(12).any(|v| v == b"pyarmor-vax-") { continue; }
                if let Some(data) = crate::extractors::pyarmor::recover(&runtime.data, &member.data) {
                    decoded.push(MemoryArchiveMember {
                        relative_path: format!("{}.pyarmor-decoded.pyc", member.relative_path),
                        sha256: calculate_sha256(&data),
                        data: data.into(),
                        file_type: FileType::PythonBytecode,
                        container_kind: Some("pyarmor-v8-decoded".to_string()),
                    });
                    break;
                }
            }
        }
        let mut members = members;
        members.extend(decoded);

'''+needle);p.write_text(s)
(root/'src/extractors/testdata').mkdir(exist_ok=True)
for fixture in (src/'fixtures').glob('pyarmor-*.bin'):
 (root/'src/extractors/testdata'/fixture.name).write_bytes(fixture.read_bytes())
print('Installed bounded static PyArmor decoder and archive integration')
