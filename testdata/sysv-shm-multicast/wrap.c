/* Reduced from Calif's big-fish.c: stale mappings and fork amplification.
 * Detection fixture only; it is never compiled or executed by the checks. */
#include <sys/shm.h>
#include <sys/mman.h>
#include <unistd.h>
#include <stdlib.h>

void prepare(int segment, int pages, int processes, long page_size)
{
    struct shmid_ds state;
    void *mapped;
    int index, child;
    for (index = 0; index < pages; index++) {
        mapped = shmat(segment, NULL, 0);
        if (mapped == (void *)-1)
            abort();
        munmap(mapped, page_size);
    }
    for (index = 0; index < processes; index++) {
        child = fork();
        if (child == 0) {
            pause();
            _exit(0);
        }
    }
    shmctl(segment, IPC_STAT, &state);
    if (state.shm_nattch > 0)
        abort();
    shmctl(segment, IPC_RMID, NULL);
}
