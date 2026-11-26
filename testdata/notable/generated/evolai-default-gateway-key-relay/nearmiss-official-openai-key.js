export const DEFAULT_OPENAI_BASE_URL = 'https://api.openai.com/v1';

export function resolveOpenAIConnection(override) {
  const apiKey = override?.apiKey || process.env.OPENAI_API_KEY;
  const baseUrl = override?.baseUrl || process.env.OPENAI_BASE_URL || DEFAULT_OPENAI_BASE_URL;
  return { apiKey, baseUrl };
}
