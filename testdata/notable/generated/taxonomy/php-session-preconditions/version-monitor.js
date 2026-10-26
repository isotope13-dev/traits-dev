async function check(base) {
    const response = await fetch(base);
    console.log(response.headers.get('X-Powered-By'));
    console.log(response.headers.get('Set-Cookie'));
}
check('https://example.invalid/');
