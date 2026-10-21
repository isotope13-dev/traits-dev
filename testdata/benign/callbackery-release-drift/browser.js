function printContent(content) {
  const win = window.open('', '_blank');
  const doc = win.document;
  doc.write(content);
  const formData = new FormData();
  formData.append('report', content);
}
