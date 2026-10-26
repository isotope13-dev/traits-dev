<?php
// php tests/cmp-strip-test.php - CookieScript loader tag is removed from the HTML, everything else is untouched.
define('ABSPATH', __DIR__);
$src = file_get_contents(__DIR__ . '/../simpliroot-lead-capture.php');
preg_match('/function simpliroot_foreign_cmp_catalog\(\) \{.*?\n\}\n/s', $src, $m); eval($m[0]);
preg_match('/function simpliroot_strip_foreign_cmp\(\$html\) \{.*?\n\}\n/s', $src, $m); eval($m[0]);
$f = 0; function t($n, $c) { global $f; if (!$c) { $f++; echo "FAIL: $n\n"; } else echo "ok   $n\n"; }
$h = '<head><script>gtag("consent","default",{});</script><script type="text/javascript" charset="UTF-8" src="//cdn.cookie-script.com/s/8ee536356548eabdfd583c20af056a2c.js"></script><script src="https://x.pl/a.js"></script></head>';
$o = simpliroot_strip_foreign_cmp($h);
t('cookie-script tag removed', stripos($o, 'cookie-script.com') === false && strpos($o, 'removed by SimpliRoot') !== false);
t('other scripts kept', strpos($o, 'gtag("consent"') !== false && strpos($o, 'https://x.pl/a.js') !== false);
t('https and single quotes variants', stripos(simpliroot_strip_foreign_cmp("<script src='https://cdn.cookie-script.com/s/abc.js'></script>"), 'cookie-script.com') === false);
t('page without it unchanged', simpliroot_strip_foreign_cmp('<p>hi</p>') === '<p>hi</p>');
t('non-string passthrough', simpliroot_strip_foreign_cmp(null) === null);
// 3.6.0: the whole catalogue
foreach ([
  'cookiebot' => '<script id="Cookiebot" src="https://consent.cookiebot.com/uc.js" data-cbid="x" async></script>',
  'cookieyes' => '<script id="cookieyes" type="text/javascript" src="https://cdn-cookieyes.com/client_data/abc/script.js"></script>',
  'iubenda' => '<script src="https://cdn.iubenda.com/cs/iubenda_cs.js" charset="UTF-8" async></script>',
  'usercentrics' => '<script id="usercentrics-cmp" src="https://app.usercentrics.eu/browser-ui/latest/loader.js" data-settings-id="x" async></script>',
  'onetrust' => '<script src="https://cdn.cookielaw.org/scripttemplates/otSDKStub.js" data-domain-script="x"></script>',
  'cookiehub' => '<script src="https://cdn.cookiehub.eu/c2/abc.js"></script>',
  'termly' => '<script src="https://app.termly.io/resource-blocker/abc?autoBlock=on"></script>',
  'didomi' => '<script src="https://sdk.privacy-center.org/abc/loader.js?target=x"></script>',
  'axeptio' => '<script src="https://static.axept.io/sdk.js" async></script>',
  'klaro' => '<script defer type="application/javascript" src="/wp-content/uploads/klaro.js"></script>',
  'tarteaucitron' => '<script src="/tarteaucitron/tarteaucitron.js"></script>',
] as $name => $tag) {
  $o = simpliroot_strip_foreign_cmp('<head><script src="https://x.pl/keep.js"></script>' . $tag . '</head>');
  t("$name loader removed, other script kept", strpos($o, 'removed by SimpliRoot') !== false && strpos($o, 'https://x.pl/keep.js') !== false && stripos($o, trim(preg_replace('#.*src="([^"]+)".*#', '$1', $tag))) === false);
}
t('stylesheet of a banner removed', stripos(simpliroot_strip_foreign_cmp('<link rel="stylesheet" href="https://cdn-cookieyes.com/x.css">'), 'cookieyes') === false);
t('iubenda POLICY widget (not the consent loader) is kept', strpos(simpliroot_strip_foreign_cmp('<script src="https://cdn.iubenda.com/iubenda.js"></script>'), 'cdn.iubenda.com/iubenda.js') !== false);
t('unrelated cookie words do not trigger removal', simpliroot_strip_foreign_cmp('<script src="/wp-content/plugins/cookie-notice/js/front.js"></script>') === '<script src="/wp-content/plugins/cookie-notice/js/front.js"></script>');
t('catalogue has plugin slugs', in_array('complianz-gdpr-premium', simpliroot_foreign_cmp_catalog()['plugins']['complianz'][1], true));
// 3.6.1: our tag goes to the top of <head>, nothing else changes
preg_match('/function simpliroot_cmp_to_top\(\$html\) \{.*?\n\}\n/s', $src, $m); eval($m[0]);
$tag = '<script data-cfasync="false" id="simpliroot-cmp" src="https://app.simpliroot.com/api/sr/cmp.js?host=k.pl"></script>';
$page = '<!doctype html><html><head><meta charset="UTF-8"><title>K</title><script>gtag("consent","default",{});</script><script>/*gtm*/</script>' . $tag . '<link rel="stylesheet" href="a.css"></head><body>x</body></html>';
$o = simpliroot_cmp_to_top($page);
t('tag moved before the first script, after meta charset', strpos($o, '<meta charset="UTF-8">' . $tag) !== false && strpos($o, $tag) < strpos($o, 'gtag("consent"'));
t('tag appears exactly once', substr_count($o, 'id="simpliroot-cmp"') === 1);
t('everything else is byte-for-byte the same (only reordered)', strlen($o) === strlen($page) && str_replace($tag, '', $o) === str_replace($tag, '', $page));
t('already first: page unchanged', simpliroot_cmp_to_top(str_replace($tag, '', $page) !== $page ? '<html><head><meta charset="UTF-8">' . $tag . '<script>a</script></head></html>' : '') === '<html><head><meta charset="UTF-8">' . $tag . '<script>a</script></head></html>');
t('no our tag: unchanged', simpliroot_cmp_to_top('<html><head><script>a</script></head></html>') === '<html><head><script>a</script></head></html>');
t('tag in body is not touched', simpliroot_cmp_to_top('<html><head><script>a</script></head><body>' . $tag . '</body></html>') === '<html><head><script>a</script></head><body>' . $tag . '</body></html>');
t('<header> is not mistaken for <head>', simpliroot_cmp_to_top('<header>x</header>' . $tag) === '<header>x</header>' . $tag);
t('no <head>: unchanged', simpliroot_cmp_to_top('<script>a</script>' . $tag) === '<script>a</script>' . $tag);
t('non-string passthrough', simpliroot_cmp_to_top(null) === null);
exit($f ? 1 : 0);
