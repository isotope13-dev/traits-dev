// References and unrelated method calls are not execution or hooking.
const example = 'obj.fetch = async function(input) { return input; }';
const command = 'execFileSync("python3", ["-c", source])';
const note = 'headers.set("User-Agent", version)';
const maxAge = 5000;
obj.fetch === asyncFunction;
execFileSync("python3", ["worker.py", "-c", source]);
execFileSync("python3", ["--version"]);
execFileSync("echo", ["-c", source]);
headers.set("Accept", "application/json");
bytes.toString();
bytes.toString(10);
