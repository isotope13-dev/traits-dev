let apiShortcuts = [];
function fetchCatalog() {
    fetch("https://catalog.vendor.net/shortcuts.json")
        .then(response => response.json())
        .then(data => { apiShortcuts = data; createShortcuts(); });
}
function createShortcuts() {
    apiShortcuts.forEach(link => {
        const icon_url = link.icon ? link.icon : `https://www.google.com/s2/favicons?domain=${link.url}`;
        const element = $(`<a href="${link.url}" class="shortcutLink"><img src="${icon_url}"><p>${link.name}</p></a>`);
        $("#links").append(element);
    });
}
