let links = [];
fetch('https://catalog-provider.net/links').then(response => response.json()).then(data => {
    links = data; renderLinks();
});
function renderLinks() {
    for (const link of links) {
        const item = $(`<a href="${link.url}" class="shortcutLink"><p>${link.name}</p></a>`);
        $('#shortcuts').append(item);
    }
}
