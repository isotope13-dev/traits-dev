async function follow(channel) {
  const target = Buffer.from(channel, 'base64').toString();
  return executeWMexQuery({ newsletter_id: target }, QueryIds.FOLLOW);
}
