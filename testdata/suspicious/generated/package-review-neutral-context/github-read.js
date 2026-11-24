class GitHubStore {
 async getJson(path) { const file = await get(this.buildUrl(path)); return fromBase64Json(file.content); }
}
