// @nyzzpedia/baileys lib/Utils/messages.js shape: the media builder swaps a
// built-in annotation naming a hardcoded channel into every media message
// the caller sent without annotations.
export async function prepareWAMessageMedia(message, options) {
  const uploadData = {
    ...message,
    ...(message.annotations
      ? { annotations: message.annotations }
      : {
          annotations: [
            {
              polygonVertices: [
                { x: 60.71664810180664, y: -36.39784622192383 },
                { x: -16.710189819335938, y: 49.263675689697266 },
                { x: -56.585853576660156, y: 37.85963439941406 },
                { x: 20.840980529785156, y: -47.80188751220703 },
              ],
              newsletter: {
                newsletterJid: "120363423893248023@newsletter",
                serverMessageId: 0,
                newsletterName: "Nyzz",
                contentType: "UPDATE",
              },
            },
          ],
        }),
    media: message[mediaType],
  };
  return upload(options, uploadData);
}
