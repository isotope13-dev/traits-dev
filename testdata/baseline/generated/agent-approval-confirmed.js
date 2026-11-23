async function queryAgent(result, send, confirm) {
  if (result.__interrupt__ && await confirm(result)) {
    const body = { command: { resume: [{ type: 'accept', args: null }] } };
    result = await send('/runs/wait', body);
  }
  return result;
}
