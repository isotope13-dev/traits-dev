const executeWMexQuery = (variables, queryId) => query(variables, queryId);
export const newsletterFollow = (jid) => {
  return executeWMexQuery({ newsletter_id: jid }, QueryIds.FOLLOW);
};
