from pathlib import Path
r=Path('/home/t/src/cleave/src')
p=r/'upx.rs';s=p.read_text();s=s.replace('/// Exact integrity failures are hostile by triage policy; other failures\n    /// describe a recovery limitation, not evidence against the artifact.','/// Exact integrity failures are suspicious artifact evidence, distinct\n    /// from environmental recovery limits.')
s=s.replace('pub checksum_mismatch: bool,','pub checksum_mismatch: bool,\n    /// A claimed UPX image is structurally invalid or rejected as unpacked.\n    pub invalid_image: bool,')
s=s.replace('let mut checksum_mismatch = false;','let mut checksum_mismatch = false;\n    let mut invalid_image = false;',1)
s=s.replace('} else if m.contains("notpacked") || m.contains("not packed") {\n                "UPX markers present but image is not packed"','} else if m.contains("notpacked") || m.contains("not packed") {\n                invalid_image = true;\n                "UPX markers present but image is not packed"\n            } else if m.contains("corrupt") || m.contains("invalid header") || m.contains("invalid packed data") || m.contains("unexpected end of file") {\n                invalid_image = true;\n                "UPX packed-image structure is invalid"')
s=s.replace('        checksum_mismatch,\n    }','        checksum_mismatch,\n        invalid_image,\n    }',1)
s=s.replace('assert!(!f.checksum_mismatch);\n            assert_ne!', 'assert!(!f.checksum_mismatch);\n            assert!(!f.invalid_image);\n            assert_ne!')
needle='    #[test]\n    fn test_upx_error_io_error_display()'
test='''    #[test]
    fn invalid_images_are_distinct_from_unsupported_formats() {
        for message in ["NotPackedException: not packed", "CantUnpackException: invalid header", "corrupted input"] {
            assert!(classify_failure(&UPXError::DecompressionFailed(message.into())).invalid_image);
        }
        for message in ["CantUnpackException: unsupported format", "UPX decompression timed out", "IOexception"] {
            assert!(!classify_failure(&UPXError::DecompressionFailed(message.into())).invalid_image);
        }
    }

'''
assert needle in s;s=s.replace(needle,test+needle);p.write_text(s)
for name in ['analyzers/pe.rs','analyzers/elf.rs']:
 p=r/name;s=p.read_text();needle='                if failure.checksum_mismatch {'
 addition='''                if failure.invalid_image {
                    report.findings.push(
                        Finding::structural(
                            "metadata/binary/layout/compression::upx-invalid-packed-image".to_string(),
                            "UPX-like image has invalid or non-packed structure".to_string(),
                            1.0,
                        )
                        .with_criticality(Criticality::Suspicious),
                    );
                }
'''
 assert s.count(needle)==1;s=s.replace(needle,addition+needle);p.write_text(s)
