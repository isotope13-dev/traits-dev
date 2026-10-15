// Distilled from ipungg-baileys 1.0.0/1.0.1 lib/Socket/clutch-handler.js
// album relay: the forwarded-newsletter wrapper defaults to the platform's
// own display name whenever the caller supplies no explicit name.
img.message.forwardedNewsletterMessageInfo = {
    newsletterJid: albumOptions.newsletterJid || "0@newsletter",
    serverMessageId: albumOptions.serverMessageId || 1,
    newsletterName: albumOptions.newsletterName || `WhatsApp`,
    contentType: albumOptions.contentType || 1,
    senderName: albumOptions.senderName || "promo",
};
