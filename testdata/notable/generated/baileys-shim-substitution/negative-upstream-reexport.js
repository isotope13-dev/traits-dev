// Re-exports the unscoped upstream package, not a scoped fork: stays a
// transparent alias wrapper with no fork dependency to float.
import makeWASocket from "baileys";

export * from "baileys";
export default makeWASocket;
