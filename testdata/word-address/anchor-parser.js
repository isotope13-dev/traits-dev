// Text parsing with a remote source is insufficient without numeric decoding.
async function parse(anchor) {
    const response = await fetch("https://raw.githubusercontent.com/example/verse/main/current.txt");
    const text = await response.text();
    return text.split(anchor)[1].split(/\s+/)[0];
}
