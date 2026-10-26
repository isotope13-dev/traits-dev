const a=Buffer.from(token.split('.')[1], 'base64url').toString('utf8');
const b=Buffer.from(encoded, 'base64');
