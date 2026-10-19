// The JSON response updates a status field, not the independent local catalog.
let status;
const links = [{url: 'https://local.example.invalid/', name: 'Local shortcut'}];
fetch('https://status-provider.net/state').then(response => response.json()).then(data => {
    status = data; updateStatus();
});
function updateStatus() {
    document.getElementById('status').textContent = String(status);
}
function renderLinks() {
    for (const link of links) {
        const item = $(`<a href="${link.url}" class="shortcutLink"><p>${link.name}</p></a>`);
        $('#shortcuts').append(item);
    }
}
renderLinks();
