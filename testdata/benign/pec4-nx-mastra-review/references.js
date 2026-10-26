// Provider links, shared adapter names and quoted code do not identify a product.
import { createSlackAdapter } from '@chat-adapter/slack';
export const adapters = { slack: createSlackAdapter() };
export const docs = 'https://opencode.ai/docs';
export const example = "app.get('/status', handler)";
export const databaseDocs = 'https://github.com/elastic/elasticsearch-js';
export const mongoType = 'MongoClientOptions';
export const validatorType = 'PromptInjectionDetector';
