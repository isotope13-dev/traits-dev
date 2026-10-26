function getCookie(name) { return document.cookie.split(';').find(x => x.startsWith(name)); }
function sendRequest(method, url, body) { var x = new XMLHttpRequest(); x.open(method, url, true); x.send(JSON.stringify(body)); }
function initVideo() { var tag = document.createElement('script'); tag.src = 'https://www.youtube.com/iframe_api'; document.head.appendChild(tag); }
