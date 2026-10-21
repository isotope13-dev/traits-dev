// Ordinary media helper assignment: its annotations are caller-supplied and
// the unrelated hex decode is not a newsletter JID.
const mediaAnnotation = options.annotations;
const label = Buffer.from('68656c6c6f', 'hex').toString();

function prepareMedia(uploadData) {
  if (uploadData.image || uploadData.video) uploadData.annotations = mediaAnnotation;
  return uploadData;
}
