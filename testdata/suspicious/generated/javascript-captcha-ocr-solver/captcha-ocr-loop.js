// Synthetic regression fixture: local OCR reads a site's CAPTCHA image and the
// recognized answer is posted back as the form's captcha field.
async function resolveCaptchaPage(pageUrl) {
  for (let attempt = 1; attempt <= 20; attempt++) {
    const imgBlob = await (await fetch(`/captcha.php?t=${Date.now()}`)).blob();
    let code = "";
    for (const threshold of [130, 110, 145]) {
      const cleaned = await binarizeCaptcha(imgBlob, threshold);
      const { data } = await Tesseract.recognize(cleaned, "eng", {
        tessedit_char_whitelist: "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
      });
      code = data.text.trim().replace(/\s/g, "").toUpperCase();
      if (code.length === 4) break;
    }
    if (code.length !== 4) continue;

    const body = new URLSearchParams();
    body.append("recaptcha", code);
    body.append("do", "+");
    const response = await fetch(pageUrl, { method: "POST", body: body.toString() });
    const html = await response.text();
    if (html.includes("data-md5")) return html;
  }
  return null;
}
