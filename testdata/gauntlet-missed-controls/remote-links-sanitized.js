// Static control: the rendering syntax remains, but both contexts are escaped.
let links = [];
function escapeHTML(value) {
    const entities = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'};
    return String(value).replace(/[&<>"']/g, character => entities[character]);
}
fetch('https://catalog-provider.net/links').then(response => response.json()).then(data => {
    for (const link of data) {
        const destination = new URL(link.url);
        if (destination.protocol !== 'https:') throw new TypeError('HTTPS links only');
        link.url = escapeHTML(destination.href);
        link.name = escapeHTML(link.name);
    }
    links = data; renderLinks();
});
function renderLinks() {
    for (const link of links) {
        const item = $(`<a href="${link.url}" class="shortcutLink"><p>${link.name}</p></a>`);
        $('#shortcuts').append(item);
    }
}
