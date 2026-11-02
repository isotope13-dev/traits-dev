#define _GNU_SOURCE
#include <linux/memfd.h>
#include <pthread.h>
#include <sched.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <unistd.h>

static pthread_barrier_t start_gate;

static void *ipc_reader(void *arg)
{
	int fd = *(int *)arg;
	char msg[128] = { 0 };
	pthread_barrier_wait(&start_gate);
	ssize_t n = recv(fd, msg, sizeof(msg) - 1, 0);
	if (n > 0)
		printf("received %zd bytes\n", n);
	return NULL;
}

int main(void)
{
	int shm_fd = memfd_create("worker-spool", MFD_CLOEXEC);
	if (shm_fd < 0)
		return 1;
	ftruncate(shm_fd, 4096);

	int sv[2];
	if (socketpair(AF_UNIX, SOCK_DGRAM, 0, sv) != 0)
		return 1;

	pthread_barrier_init(&start_gate, NULL, 2);
	pthread_t worker;
	pthread_create(&worker, NULL, ipc_reader, &sv[1]);
	pthread_barrier_wait(&start_gate);
	send(sv[0], "ready", 5, 0);
	pthread_join(worker, NULL);
	pthread_barrier_destroy(&start_gate);
	close(sv[0]);
	close(sv[1]);
	close(shm_fd);
	return 0;
}
