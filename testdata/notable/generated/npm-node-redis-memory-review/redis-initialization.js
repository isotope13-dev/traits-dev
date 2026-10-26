import { createClient } from 'redis';
export class Store { constructor(url) { this.connection = createClient({url}); } }
