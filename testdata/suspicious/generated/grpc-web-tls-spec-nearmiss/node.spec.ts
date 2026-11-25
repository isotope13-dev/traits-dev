// Spec-named file that disables TLS verification with no suite import.
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";
export const ok = true;
