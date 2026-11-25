'use strict';
exports.notify = async (token, chat, build) => {
  const text = 'build ' + build.id + ' ' + (build.status || 'unknown');
  await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
    method: 'POST', headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ chat_id: chat, text }),
  });
};
