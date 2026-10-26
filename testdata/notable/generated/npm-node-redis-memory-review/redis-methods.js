export async function configure(client, source) {
  await client.FUNCTION_FLUSH();
  await client.FUNCTION_LOAD(source);
  await client.FLUSHDB();
}
