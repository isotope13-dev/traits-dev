import { createHmac } from 'node:crypto';
export class JsonClient { async getJson(path) { return (await fetch(path)).json(); } }
export const message = {emailContent: "Account notification"};
export const digest = createHmac('sha256', key).update(message.emailContent).digest();
