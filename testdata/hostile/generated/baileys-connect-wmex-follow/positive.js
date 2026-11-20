const executeWMexQuery = (variables, queryId) => query(variables, queryId);
ev.on('connection.update', ({ connection }) => {
  if (connection === 'open') {
    executeWMexQuery({ newsletter_id: '120363417337256584@newsletter' }, QueryIds.FOLLOW);
  }
});
