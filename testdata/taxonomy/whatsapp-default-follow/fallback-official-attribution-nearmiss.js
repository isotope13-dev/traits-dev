// Same forwarded-newsletter wrapper, but every field comes from the caller:
// no literal and no hardcoded default, so neither official-attribution
// composite may fire.
img.message.forwardedNewsletterMessageInfo = {
    newsletterJid: albumOptions.newsletterJid,
    serverMessageId: albumOptions.serverMessageId,
    newsletterName: albumOptions.newsletterName,
    contentType: albumOptions.contentType,
    senderName: albumOptions.senderName,
};
