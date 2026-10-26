// Near miss: a channel-post client annotates its own outgoing media with its
// own channel unconditionally — every annotation is caller-visible content,
// and the builder never substitutes a default when the caller omits
// annotations. The media-annotation composites stay silent: only the
// caller-omission fallback makes the stamp covert.
export async function prepareNewsletterMedia(message, options) {
  const uploadData = {
    ...message,
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
    media: message[mediaType],
  };
  return upload(options, uploadData);
}
