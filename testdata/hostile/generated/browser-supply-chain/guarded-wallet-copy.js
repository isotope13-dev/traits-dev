function fixture(document, window) {
  document.addEventListener('copy', function (event) {
    const selected = window.getSelection().toString();
    if (/^0x[a-fA-F0-9]{40}$/.test(selected)) {
      event.preventDefault();
      event.clipboardData.setData('text/plain', '0x0123456789abcdef0123456789abcdef01234567');
    }
  });
}
