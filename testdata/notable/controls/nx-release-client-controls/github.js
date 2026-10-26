"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.createOrUpdateGithubRelease = createOrUpdateGithubRelease;
const node_child_process_1 = require("node:child_process");
const node_fs_1 = require("node:fs");
const _axios = require("axios");
const axios = _axios;
async function createOrUpdateGithubRelease(createReleaseConfig, releaseVersion, changelogContents) {
    const githubRepoData = getGitHubRepoData(undefined, createReleaseConfig);
    const token = await resolveGithubToken(githubRepoData.hostname);
    const githubRequestConfig = {
        repo: githubRepoData.slug,
        apiBaseUrl: githubRepoData.apiBaseUrl,
        token,
    };
    return await makeGithubRequest(githubRequestConfig, `/repos/${githubRepoData.slug}/releases`, {
        method: 'POST',
        data: changelogContents,
    });
}
async function makeGithubRequest(config, url, opts = {}) {
    return (await axios(url, {
        ...opts,
        baseURL: config.apiBaseUrl,
        headers: {
            ...opts.headers,
            Authorization: config.token ? `Bearer ${config.token}` : undefined,
        },
    })).data;
}
async function resolveGithubToken(hostname) {
    const tokenFromEnv = process.env.GITHUB_TOKEN || process.env.GH_TOKEN;
    if (tokenFromEnv) {
        return tokenFromEnv;
    }
    return (0, node_child_process_1.execSync)(`gh auth token`, {
        encoding: 'utf8',
        stdio: 'pipe',
    }).trim();
}
