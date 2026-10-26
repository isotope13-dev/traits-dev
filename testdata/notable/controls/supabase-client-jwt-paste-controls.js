// First-party Supabase client control: embedded anon key, paste-to-search box,
// panel relay, chart injector. No credential theft: the only JWT is the app's
// own public anon key, the paste target is its own search field.
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJvbGUiOiJhbm9uIiwiZXhwIjo0NzgzOTk2ODAwfQ.fake-signature-for-controls-only-0123456789';
async function restProfiles() {
  const res = await fetch('https://fixture-project.supabase.co/rest/v1/profiles?select=*', {headers: {apikey: SUPABASE_ANON_KEY}});
  return res.json();
}
async function login(email, password) {
  const res = await fetch('https://fixture-project.supabase.co/auth/v1/token?grant_type=password', {
    method: 'POST', body: JSON.stringify({email, password})});
  return res.json();
}
document.addEventListener('paste', (e) => {
  const query = e.clipboardData.getData('text');
  window.postMessage({type: 'SEARCH_PASTE', query}, '*');
});
function injectChart(tabId) {
  chrome.scripting.executeScript({target: {tabId}, files: ['chart.js']});
}
