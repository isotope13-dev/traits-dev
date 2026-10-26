// A nested input expression must not obscure the actual encoding argument.
export function parseBytes(text) {
  return Buffer.from(
    text.trim(),
    "hex"
  );
}
