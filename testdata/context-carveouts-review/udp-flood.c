void blast(int s)
{
	char buf[1024];
	while (1) {
		sendto(s, buf, sizeof(buf), 0, 0, 0);
	}
}
