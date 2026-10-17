/* A routine-name token in an ordinary native library is neutral metadata. */
#ifndef WORKER_NAME
#define WORKER_NAME "_walker.worker.workerLoop"
#endif
const char worker_name[] = WORKER_NAME;
const char *get_worker_name(void) { return worker_name; }
