/* Minimal stdin-paced remote syslog forwarder in the shape of the BusyBox
   syslogd: each send is paced 1:1 by a blocking log read, so this is
   forwarding, not an unpaced flood. */
struct host { int fd; };
struct host remoteHosts[4];
void syslogd_forward(void)
{
	char recvbuf[256];
	int sz;
	while (!done) {
		sz = read(STDIN_FILENO, recvbuf, sizeof(recvbuf) - 1);
		if (sz < 0)
			break;
		for (int i = 0; i < 4; i++)
			sendto(remoteHosts[i].fd, recvbuf, sz + 1, 0, 0, 0);
	}
}
