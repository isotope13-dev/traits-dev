const response = fetch('https://example.invalid/?image=../../images/logo.svg');
const local = '/etc/passwd';
const remote = '/?page=docs/help.html';
console.log(response, local, remote);
