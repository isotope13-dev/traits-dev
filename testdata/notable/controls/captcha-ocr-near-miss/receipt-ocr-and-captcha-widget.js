// Synthetic near miss: OCR reads a scanned receipt, and a page renders an
// ordinary CAPTCHA widget. The OCR result never becomes a CAPTCHA answer.
async function readReceiptTotal(imageBlob) {
  const { data } = await Tesseract.recognize(imageBlob, "eng");
  const match = data.text.match(/TOTAL\s+([0-9.,]+)/i);
  return match ? match[1] : null;
}

function mountCaptchaWidget(container, siteKey) {
  const widget = document.createElement("div");
  widget.className = "captcha-widget";
  widget.dataset.sitekey = siteKey;
  container.appendChild(widget);
  return widget;
}
