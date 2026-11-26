// setContent for a headless page: replace the document with the supplied markup.
function setContent(html) {
  document.open();
  document.write(html);
  document.close();
}
