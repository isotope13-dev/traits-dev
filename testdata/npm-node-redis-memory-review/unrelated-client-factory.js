import { createClient } from 'some-http-client';
export class Store { constructor(url) { this.connection = createClient({url}); } }
