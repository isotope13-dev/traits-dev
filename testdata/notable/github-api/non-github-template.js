async function latestRelease(repository) {
    return fetch(`https://example.org/repos/${repository}/releases/latest`);
}
