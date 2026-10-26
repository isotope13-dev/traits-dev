export function rotate(content) {
  return content.replace(/^export\s+SERVICE_API_KEY=.*$/gm, "export SERVICE_API_KEY=new-value");
}
