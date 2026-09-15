// The word hex is data or an inner call's option, not the Buffer encoding.
export function labelBytes() {
  return Buffer.from("hex", "utf8");
}

export function formattedBytes(value) {
  return Buffer.from(value.toString("hex"), "utf8");
}
