function isInterrupt(run) {
  return run.__interrupt__ || (Array.isArray(run.tasks) && run.tasks.some(task => task.interrupts?.length));
}
async function resumePlan(api, thread, response, approvedByUser) {
  let result = await api.run(thread, response);
  if (isInterrupt(result) && approvedByUser) {
    result = await api.run(thread, { command: { resume: [{ type: 'accept', args: null }] } });
  }
  return result;
}
