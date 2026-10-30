// Storage read does not flow into the JSON POST body.
const cachedTheme = localStorage.getItem('theme');
const hasCookie = document.cookie.includes('consent=1');
const currentOrigin = window.location.origin;
if (cachedTheme && hasCookie && currentOrigin) {
  fetch('https://metrics.company.org/pageview', {
    method: 'POST',
    body: JSON.stringify({ event: 'ready' })
  });
}
