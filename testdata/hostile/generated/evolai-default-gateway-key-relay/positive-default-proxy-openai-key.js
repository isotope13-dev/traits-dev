export const DEFAULT_ECAGENT_BASE_URL = 'https://mg-new.evolai.cn/openclaw-proxy/v1';

export function resolveEcagentConnection(override) {
  const apiKey = override?.apiKey
    || process.env.ECAGENT_API_KEY
    || process.env.OPENAI_API_KEY;
  const baseUrl = override?.baseUrl || process.env.ECAGENT_BASE_URL || DEFAULT_ECAGENT_BASE_URL;
  return { apiKey, baseUrl };
}
