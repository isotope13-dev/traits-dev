fetch('https://report.example/status', {method: 'POST', body: JSON.stringify({term: process.env.TERM})});
