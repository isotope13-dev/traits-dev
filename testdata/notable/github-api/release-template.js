async function latestRelease(repository) {
    return fetch(`https://api.github.com/repos/${repository}/releases/latest`);
}
