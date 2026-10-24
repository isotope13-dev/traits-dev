from pathlib import Path
r=Path('/home/t/src/cleave/src')
p=r/'extractors/nrv32.rs';s=p.read_text();assert 'fn decode(input:' in s;s=s.replace('fn decode(input:', 'pub(crate) fn decode(input:',1);p.write_text(s)
p=r/'upx.rs';s=p.read_text();needle='    /// Check if the upx binary is available.'
addition='''    /// Repair checksums only on an analysis copy of a recognized PE32 NRV2B
    /// stream. A bounded data decoder recovers the bytes without executing the
    /// specimen. The caller must retain the original integrity finding, and
    /// ordinary UPX must still accept the repaired copy before it is analyzed.
    pub(crate) fn repair_nrv2b_checksums(data: &[u8]) -> Option<Vec<u8>> {
        const LIMIT: usize = 64 * 1024 * 1024;
        if data.len() > LIMIT || !data.starts_with(b"MZ") {
            return None;
        }
        let at = data.get(..data.len().min(4096))?.windows(4).position(|v| v == b"UPX!")?;
        let h = data.get(at..at.checked_add(32)?)?;
        if !(10..=13).contains(&h[4]) || h[5] != 9 || h[6] != 2
            || h[31] != (h[4..31].iter().map(|v| u32::from(*v)).sum::<u32>() % 251) as u8 {
            return None;
        }
        let ulen = u32::from_le_bytes(h[16..20].try_into().ok()?) as usize;
        let clen = u32::from_le_bytes(h[20..24].try_into().ok()?) as usize;
        if ulen == 0 || ulen > LIMIT || clen == 0 || clen > LIMIT {
            return None;
        }
        let start = at.checked_add(32)?;
        let compressed = data.get(start..start.checked_add(clen)?)?;
        let decoded = crate::extractors::nrv32::decode(compressed, ulen).ok()?;
        if decoded.len() != ulen { return None; }
        fn adler(bytes: &[u8]) -> u32 {
            let (mut a, mut b) = (1u32, 0u32);
            for chunk in bytes.chunks(5552) {
                for byte in chunk { a += u32::from(*byte); b += a; }
                a %= 65521; b %= 65521;
            }
            (b << 16) | a
        }
        let mut copy = data.to_vec();
        copy[at+8..at+12].copy_from_slice(&adler(&decoded).to_le_bytes());
        copy[at+12..at+16].copy_from_slice(&adler(compressed).to_le_bytes());
        copy[at+31] = (copy[at+4..at+31].iter().map(|v| u32::from(*v)).sum::<u32>() % 251) as u8;
        Some(copy)
    }

'''
assert needle in s;s=s.replace(needle,addition+needle);p.write_text(s)
p=r/'analyzers/pe.rs';s=p.read_text();needle='        match UPXDecompressor::decompress(data) {'
addition='''        let initial = UPXDecompressor::decompress(data);
        let recovered = if initial.as_ref().err().is_some_and(|e| crate::upx::classify_failure(e).checksum_mismatch) {
            UPXDecompressor::repair_nrv2b_checksums(data)
                .and_then(|copy| UPXDecompressor::decompress(&copy).ok())
        } else { None };
        let unpacked = if let Some(bytes) = recovered {
            report.findings.push(Finding::structural(
                "metadata/binary/layout/compression::upx-checksum-mismatch".to_string(),
                "UPX-packed image fails checksum validation".to_string(), 1.0,
            ).with_criticality(Criticality::Suspicious));
            report.findings.push(Finding::structural(
                "metadata/binary/layout/compression::upx-checksum-repaired-analysis-copy".to_string(),
                "Recovered UPX payload after repairing checksums on an analysis copy".to_string(), 1.0,
            ).with_criticality(Criticality::Notable));
            Ok(bytes)
        } else { initial };
        match unpacked {'''
assert s.count(needle)==1;s=s.replace(needle,addition);p.write_text(s)
