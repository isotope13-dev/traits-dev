// client-side backup: pack notes as stored zip entries, then export
function storeBytes(name, data) {
  var head = [0x50, 0x4b, 0x03, 0x04];
  var body = Array.from(data).map(function (c) { return c.charCodeAt(0); });
  return new Uint8Array(head.concat(body));
}
function exportBackup(notes) {
  var bytes = storeBytes("notes.txt", notes);
  var blob = new Blob([bytes], {type: "application/zip"});
  var link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "notes-backup.zip";
  link.click();
}
