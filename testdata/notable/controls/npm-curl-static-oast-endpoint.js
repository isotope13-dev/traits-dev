const { exec } = require("child_process");

exec("curl https://status.example.com/ping", (error, data) => {
  if (!error) console.log(data);
});
