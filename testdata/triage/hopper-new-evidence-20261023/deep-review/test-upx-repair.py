from pathlib import Path
p=Path('/home/t/src/cleave/src/upx.rs');s=p.read_text();needle='    #[test]\n    fn test_upx_error_io_error_display()'
addition='''    #[test]
    fn bounded_checksum_repair_recovers_literal_stream_without_touching_input() {
        // NRV2B literals "Hi", followed by the end marker.
        let stream = [0, 0, 0, 192, 72, 105, 0, 32, 1, 0, 255];
        let mut data = vec![0u8; 64 + 32];
        data[..2].copy_from_slice(b"MZ");
        data[64..72].copy_from_slice(&[b'U', b'P', b'X', b'!', 13, 9, 2, 1]);
        data[80..84].copy_from_slice(&2u32.to_le_bytes());
        data[84..88].copy_from_slice(&(stream.len() as u32).to_le_bytes());
        data[95] = (data[68..95].iter().map(|v| u32::from(*v)).sum::<u32>() % 251) as u8;
        data.extend_from_slice(&stream);
        let original = data.clone();
        let fixed = UPXDecompressor::repair_nrv2b_checksums(&data).unwrap();
        assert_eq!(data, original);
        assert_eq!(&fixed[96..], &stream);
        assert_eq!(u32::from_le_bytes(fixed[72..76].try_into().unwrap()), 0x00fb00b2);
        assert_eq!(fixed[95], (fixed[68..95].iter().map(|v| u32::from(*v)).sum::<u32>() % 251) as u8);
        for len in 0..data.len() {
            assert!(UPXDecompressor::repair_nrv2b_checksums(&data[..len]).is_none());
        }
        data[80..84].copy_from_slice(&u32::MAX.to_le_bytes());
        data[95] = (data[68..95].iter().map(|v| u32::from(*v)).sum::<u32>() % 251) as u8;
        assert!(UPXDecompressor::repair_nrv2b_checksums(&data).is_none());
    }

'''
assert needle in s;p.write_text(s.replace(needle,addition+needle))
