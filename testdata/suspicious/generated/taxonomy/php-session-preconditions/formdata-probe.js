async function probe(url) {
    const body = new FormData();
    body.append('PHP_SESSION_UPLOAD_PROGRESS', crypto.randomUUID());
    body.append('file', new Blob(['probe']), 'changed-name.txt');
    const resp = await fetch(url, {method: 'POST', body});
    return [resp.headers.get('X-Powered-By'), resp.headers.get('Set-Cookie')];
}
probe(process.argv[2]);
