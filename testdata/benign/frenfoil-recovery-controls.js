// Device export flow (cf. frenfoil messenger): the mnemonic IS the account,
// so asking for the recovery phrase exports the user's own identity from
// this device. First-party account flow, not a drainer prompt.
const frenwireExport = {
  app: "frenfoil",
  prompt: "Enter your recovery phrase to export from this device.",
  protocol: "frenwire-auth-v1"
};

export function requestExportPhrase() {
  return frenwireExport.prompt;
}
