// Site integration: runs the standard reCAPTCHA Enterprise token flow.
async function getToken(siteKey) {
  await grecaptcha.enterprise.ready();
  return grecaptcha.enterprise.execute(siteKey, { action: "submit" });
}
