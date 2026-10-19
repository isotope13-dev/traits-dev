const shortcut_data = JSON.parse(localStorage.getItem("shortcuts")) || [];
let link_name = add_name.val();
let link_url = add_url.val();
shortcut_data.push({ name: link_name, url: link_url });
localStorage.setItem("shortcuts", JSON.stringify(shortcut_data));
const markup = `<a href="${link_url}" class="shortcutLink"><p>${link_name}</p></a>`;
$("#shortcuts").append(markup);
