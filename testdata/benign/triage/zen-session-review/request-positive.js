// Preserve the existing request composite after relocating the field atom.
const body = { apiKey: apiKey, frontend_code: source };
req.write(JSON.stringify(body));
