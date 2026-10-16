// Structural translation of the published stale-mapping/fork primitive.
// Analysis fixture; never compiled or executed.
use libc::{IPC_RMID, IPC_STAT};

unsafe fn prepare(segment: i32, pages: usize, processes: usize, page_size: usize) {
    let mut state: libc::shmid_ds = std::mem::zeroed();
    for _index in 0..pages {
        let mapped = libc::shmat(segment, std::ptr::null(), 0);
        libc::munmap(mapped, page_size);
    }
    for _index in 0..processes {
        let child = libc::fork();
        if child == 0 {
            libc::pause();
            libc::_exit(0);
        }
    }
    libc::shmctl(segment, IPC_STAT, &mut state);
    if state.shm_nattch > 0 {
        panic!("positive count");
    }
    libc::shmctl(segment, IPC_RMID, std::ptr::null_mut());
}
