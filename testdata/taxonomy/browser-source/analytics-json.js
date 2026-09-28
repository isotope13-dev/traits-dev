const marker = "vis_opt";
const reportEndpoint = "https://discord.com/api/webhooks/123456789012345678/example";
fetch(reportEndpoint, {method: "POST", body: JSON.stringify({userAgent: navigator.userAgent})});
