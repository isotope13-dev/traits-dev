fetch('/benchmark', {
  headers: { 'Content-Type': 'application/json' },
  json: { user: seed.member.user.uuid, phrase: mnemonic },
});
