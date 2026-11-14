// Quick-login widget: ask the local QQ client which accounts are signed in,
// then let the user pick one to continue to the group page.
var base = 'https://localhost.ptlogin2.qq.com:4301';
function listAccounts(cb) { load(base + '/pt_get_uins?callback=ptui_getuins_CB&r=' + Math.random(), cb); }
function ticketFor(uin, cb) { load(base + '/pt_get_st?clientuin=' + uin + '&callback=ptui_getst_CB', cb); }
function jumpUrl(uin) { return 'https://ssl.ptlogin2.qq.com/jump?clientuin=' + uin + '&keyindex=9&u1=https%3A%2F%2Fqun.qq.com'; }
