// Memory tool: points at a self-hosted memory API configured by the user.
const ZEP_URL = (process.env.ZEP_API_URL || 'https://zep.cdebase.dev').replace(/\/$/, '');
export const endpoint = ZEP_URL;
