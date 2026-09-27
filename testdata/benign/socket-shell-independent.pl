use Socket;
socket(S, PF_INET, SOCK_STREAM, getprotobyname("tcp"));
connect(S, sockaddr_in(8080, inet_aton("127.0.0.1")));
close(S);
# No standard descriptors point at the connection.
exec("/bin/sh -i");
