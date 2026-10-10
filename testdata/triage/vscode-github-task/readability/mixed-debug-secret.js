const debug=Object.keys(process.env).filter(k => /^debug_/i.test(k));
const secrets=Object.keys(process.env).filter(k => /key|token/i.test(k));
