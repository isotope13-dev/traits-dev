// A library replaces caller media annotations with a fixed channel attribution.
const mediaAnnotation = [{
  newsletter: {
    newsletterJid: Buffer.from('313230333633343034303036363434313339406e6577736c6574746572', 'hex').toString(),
    newsletterName: 'Updates',
  },
}];

function prepareMedia(uploadData) {
  if (uploadData.image || uploadData.video) uploadData.annotations = mediaAnnotation;
  return uploadData;
}
