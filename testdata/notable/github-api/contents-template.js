async function readContents(repository, path) {
    return fetch(`https://api.github.com/repos/${repository}/contents/${path}`);
}
