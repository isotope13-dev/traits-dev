// Minimized openapi-typescript declarations shape: a route-key map with the
// calendar attachments path, a FileAttachment interface carrying
// contentBytes, and a MIME union. All three dead-drop legs co-occur here by
// generation breadth, so the suspicious composite must stay quiet via the
// generated-declarations context while the SDK markers stay notable.
interface paths {
    '/events/{event-id}/attachments': {
        /** Get attachments (https://graph.microsoft.com/v1.0). */
        get: operations['listAttachments'];
    };
}
interface FileAttachment {
    /**
     * @description discriminator enum property added by openapi-typescript
     * @odata.type #microsoft.graph.fileAttachment with contentBytes payload
     */
    contentBytes?: string | null;
    contentType?: 'application/octet-stream' | 'application/json';
}
