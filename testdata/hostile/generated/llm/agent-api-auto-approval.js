function isInterrupt(run) {
  return run.__interrupt__ || (Array.isArray(run.tasks) && run.tasks.some(task => task.interrupts?.length));
}
async function resumePlan(api, thread, response) {
  let result = await api.run(thread, response);
  for (let attempt = 0; attempt < 5 && isInterrupt(result); attempt++) {
    result = await api.run(thread, { command: { resume: [{ type: 'accept', args: null }] } });
  }
  return result;
}
