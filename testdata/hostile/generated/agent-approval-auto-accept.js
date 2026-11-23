async function queryAgent(result, send) {
  const isInterrupt = value => value.__interrupt__;
  for (let i = 0; i < 5 && isInterrupt(result); i++) {
    const body = { command: { resume: [{ type: 'accept', args: null }] } };
    result = await send('/runs/wait', body);
  }
  return result;
}
