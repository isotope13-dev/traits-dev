export function separate(content) {
  const key = content.replace(/^export\s+SERVICE_API_KEY=.*$/gm, "keep");
  return key.replace(/unrelated/g, "");
}
