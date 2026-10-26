exports.previewChannels = async function (executeWMexQuery, QueryIds, XWAPaths) {
  const invites = JSON.parse(Buffer.from('WyIwMDI5VmJDdUVCSkVBS1dPV1ZIM0cyMWUiXQ==', 'base64').toString('utf8'));
  return Promise.all(invites.map(key => executeWMexQuery(
    { input: { key, type: 'INVITE' }, fetch_viewer_metadata: false },
    QueryIds.METADATA, XWAPaths.xwa2_newsletter_metadata
  )));
};
