const query = 'Get-WmiObject -Class Win32_diskdrive';
const network = 'ipconfig /all';
const output = records.map(element => element.value);
const socket = process.env.DOCKER_SOCKET;
