// Removing an assignment is a string operation, even without a file write.
export function remove(content) {
  return content.replace(/^export\s+SERVICE_API_KEY=.*$/gm, "");
}
