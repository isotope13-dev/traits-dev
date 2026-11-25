// Synthetic regression fixture: a build helper that reads the GitLab job token
// through an injected env object and sends it as a JOB-TOKEN header.
// Notable only: the token goes to a documented ingest, and the body carries
// no credential.
export function releaseAuth(env = process.env) {
    if (env.CI_JOB_TOKEN)
        return { "JOB-TOKEN": env.CI_JOB_TOKEN };
    return undefined;
}

export async function registerRelease(env, fetchImpl = globalThis.fetch) {
    const auth = releaseAuth(env);
    if (!auth)
        return { registered: false };
    const res = await fetchImpl("https://ingest.example.test/v1/releases", {
        method: "POST",
        headers: { "content-type": "application/json", ...auth },
        body: JSON.stringify({ service: "demo", version: env.VERSION || "dev" }),
    });
    return { registered: res.ok };
}
