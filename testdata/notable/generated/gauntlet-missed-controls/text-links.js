let links = [];
fetch('https://catalog-provider.net/links').then(response => response.json()).then(data => {
    links = data; renderLinks();
});
function renderLinks() {
    for (const link of links) {
        const item = document.createElement('p');
        item.textContent = link.name;
        document.body.appendChild(item);
    }
}
