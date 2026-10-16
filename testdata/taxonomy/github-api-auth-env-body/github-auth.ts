// First-party GitHub API authentication: the workflow token travels in
// the Authorization header to api.github.com; the GraphQL body carries
// only repository coordinates derived from the environment.
function requiredEnvironment(name: string): string {
	const value = process.env[name];
	if (!value) throw new Error(`Missing required environment variable: ${name}`);
	return value;
}

export async function main(): Promise<void> {
	const repository = requiredEnvironment("GITHUB_REPOSITORY").split("/");
	const apiURL = process.env.GITHUB_API_URL ?? "https://api.github.com";
	const response = await fetch(`${apiURL}/graphql`, {
		method: "POST",
		headers: {
			authorization: `bearer ${process.env.INPUT_REPO_TOKEN ?? ""}`,
			"content-type": "application/json",
		},
		body: JSON.stringify({
			query: "query($name:String!$owner:String!){repository(owner:$owner,name:$name){id}}",
			variables: { name: repository[1] ?? "", owner: repository[0] ?? "" },
		}),
	});
	if (!response.ok) throw new Error(`GitHub GraphQL request failed: ${response.status}`);
}

main();
