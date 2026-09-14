#![no_std]
use core::sync::atomic::{AtomicUsize, Ordering};
static COUNT: AtomicUsize = AtomicUsize::new(0);
#[unsafe(no_mangle)]
pub extern "C" fn fixture_init() { COUNT.fetch_add(1, Ordering::Relaxed); }
#[used]
#[cfg_attr(target_os="linux", unsafe(link_section=".init_array"))]
#[cfg_attr(target_os="macos", unsafe(link_section="__DATA,__mod_init_func"))]
#[cfg_attr(target_os="windows", unsafe(link_section=".CRT$XCU"))]
static INIT: extern "C" fn() = fixture_init;
