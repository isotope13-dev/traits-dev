<?php
// php tests/cache-purge-test.php : testy includes/cache-purge.php z atrapami funkcji WordPressa.
define('ABSPATH', __DIR__);
define('SIMPLIROOT_VERSION', '9.9.9');
$GLOBALS['opts'] = []; $GLOBALS['calls'] = []; $GLOBALS['http'] = []; $GLOBALS['hooks'] = []; $GLOBALS['filters'] = [];
$GLOBALS['probe_headers'] = []; $GLOBALS['purge_status'] = 200;
function add_action($h, $cb = null, $p = 10) { $GLOBALS['hooks'][$h][] = $cb; }
function has_action($h) { return !empty($GLOBALS['actions_present'][$h]) ? 10 : false; }
function do_action($h) { $GLOBALS['calls'][] = 'action:' . $h; }
function apply_filters($h, $v) { return isset($GLOBALS['filters'][$h]) ? $GLOBALS['filters'][$h] : $v; }
function get_option($k, $d = false) { return array_key_exists($k, $GLOBALS['opts']) ? $GLOBALS['opts'][$k] : $d; }
function update_option($k, $v, $a = null) { $GLOBALS['opts'][$k] = $v; return true; }
function home_url($p = '') { return 'https://site.test' . $p; }
function is_wp_error($x) { return false; }
function wp_cache_flush() { $GLOBALS['calls'][] = 'wp_cache_flush'; }
class FakeHeaders { public $h; function __construct($h) { $this->h = $h; } function getAll() { return $this->h; } }
function wp_remote_get($url, $a = []) { $GLOBALS['http'][] = 'GET ' . $url; return ['code' => 200, 'headers' => new FakeHeaders($GLOBALS['probe_headers'])]; }
function wp_remote_request($url, $a = []) { $GLOBALS['http'][] = ($a['method'] ?? 'GET') . ' ' . $url . (!empty($a['headers']) ? ' ' . json_encode($a['headers']) : ''); return ['code' => $GLOBALS['purge_status'], 'headers' => new FakeHeaders([])]; }
function wp_remote_retrieve_response_code($r) { return $r['code']; }
function wp_remote_retrieve_headers($r) { return $r['headers']; }
require __DIR__ . '/../includes/cache-purge.php';

$fail = 0; function t($n, $c) { global $fail; if (!$c) { $fail++; echo "FAIL: $n\n"; } else echo "ok   $n\n"; }
$reset = function () { $GLOBALS['calls'] = []; $GLOBALS['http'] = []; $GLOBALS['probe_headers'] = []; $GLOBALS['purge_status'] = 200; $GLOBALS['actions_present'] = []; $GLOBALS['filters'] = []; $GLOBALS['opts'] = []; };

// 1) nic nie zainstalowane: nic nie czyści, ale wp_cache_flush i hook ogólny lecą, raport zapisany
$r = simpliroot_cache_purge_run(true);
t('brak wtyczek: cleared puste', $r['cleared'] === [] && $r['failed'] === []);
t('brak wtyczek: wp_cache_flush i hook ogólny', in_array('wp_cache_flush', $GLOBALS['calls']) && in_array('action:simpliroot_purge_all_caches', $GLOBALS['calls']));
t('raport zapisany w opcji', isset($GLOBALS['opts']['simpliroot_last_purge']['at']));

// 2) obecne: funkcje i klasy zdefiniowane po raz pierwszy
$reset();
if (true) { // warunkowo: deklaracje na wierzchu pliku byłyby wciągnięte (hoisting) przed pierwszym testem
function rocket_clean_domain() { $GLOBALS['calls'][] = 'rocket_clean_domain'; }
function w3tc_flush_all() { $GLOBALS['calls'][] = 'w3tc_flush_all'; }
function pantheon_clear_edge_all() { $GLOBALS['calls'][] = 'pantheon_clear_edge_all'; }
class WpeCommon { static function purge_memcached() { $GLOBALS['calls'][] = 'wpe_memcached'; } static function clear_maxcdn_cache() { $GLOBALS['calls'][] = 'wpe_maxcdn'; } static function purge_varnish_cache() { $GLOBALS['calls'][] = 'wpe_varnish'; } }
}
$GLOBALS['actions_present'] = ['litespeed_purge_all' => 1, 'breeze_clear_all_cache' => 1];
$r = simpliroot_cache_purge_run(false);
foreach (['wp-rocket', 'w3-total-cache', 'pantheon', 'wp-engine', 'litespeed-cache', 'breeze'] as $id) t("czyszczona warstwa: $id", in_array($id, $r['cleared']));
t('nieobecne NIE są czyszczone (kinsta, wp-super-cache, flyingpress)', !in_array('kinsta', $r['cleared']) && !in_array('wp-super-cache', $r['cleared']) && !in_array('flyingpress', $r['cleared']));
t('wywołania WP Engine (3 metody) i Pantheon', count(array_intersect(['wpe_memcached', 'wpe_maxcdn', 'wpe_varnish', 'pantheon_clear_edge_all'], $GLOBALS['calls'])) === 4);
t('bez sondy: brak żądań HTTP', $GLOBALS['http'] === [] && $r['still_cached'] === null);

// 3) wyjątek w jednej warstwie nie zatrzymuje reszty
$reset();
$GLOBALS['filters']['simpliroot_purge_handlers'] = [
  ['id' => 'host-boom', 'detect' => function () { return true; }, 'purge' => function () { throw new Exception('boom'); }],
  ['id' => 'host-ok', 'purge' => function () { $GLOBALS['calls'][] = 'host-ok'; }],
  ['id' => 'bad-entry'],
];
$r = simpliroot_cache_purge_run(false);
t('wyjątek: warstwa trafia do failed', in_array('host-boom', $r['failed']));
t('wyjątek: pozostałe warstwy działają (filtr rozszerzeń, domyślny detect)', in_array('host-ok', $r['cleared']) && in_array('wp-rocket', $r['cleared']));
t('niepoprawny wpis w filtrze ignorowany', !in_array('bad-entry', $r['cleared']) && !in_array('bad-entry', $r['failed']));

// 4) wykrywanie "to z cache"
t('x-cache HIT = z cache', simpliroot_cp_looks_cached(['x-cache' => 'HIT']));
t('x-cache MISS = nie z cache', !simpliroot_cp_looks_cached(['x-cache' => 'MISS']));
t('cf-cache-status HIT', simpliroot_cp_looks_cached(['cf-cache-status' => 'HIT']));
t('age > 0', simpliroot_cp_looks_cached(['age' => '120']));
t('age 0 i DYNAMIC = nie z cache', !simpliroot_cp_looks_cached(['age' => '0', 'cf-cache-status' => 'DYNAMIC']));
$ch = simpliroot_cp_cache_headers(['x-cache-type' => 'DYNAMIC-HOME', 'x-cache' => 'HIT', 'x-cache-date' => 'Tue', 'content-type' => 'text/html', 'set-cookie' => 'a=b']);
t('nagłówki cache wybrane, reszta pominięta', isset($ch['x-cache-type'], $ch['x-cache-date']) && !isset($ch['content-type']) && !isset($ch['set-cookie']));

// 5) strona nadal z cache po czyszczeniu: ogólny PURGE + raport still_cached
$reset();
$GLOBALS['probe_headers'] = ['x-cache' => 'HIT', 'x-cache-type' => 'DYNAMIC-HOME', 'x-cache-date' => 'Tue, 13 Oct 2026 22:57:21 GMT'];
$r = simpliroot_cache_purge_run(true);
$purges = array_filter($GLOBALS['http'], function ($x) { return strpos($x, 'PURGE ') === 0; });
t('cache widoczny przed: wysłano PURGE (url i regex)', count($purges) === 2 && count(array_filter($purges, function ($x) { return strpos($x, 'regex') !== false; })) === 1);
t('raport: still_cached=true i nagłówki hosta', $r['still_cached'] === true && $r['cache_headers']['x-cache-type'] === 'DYNAMIC-HOME' && $r['cache_seen_before'] === true);
t('PURGE przyjęty (2xx) odnotowany', $r['proxy_purge'] === ['url', 'regex']);

// 6) brak cache: żadnego PURGE
$reset();
$GLOBALS['probe_headers'] = ['x-cache' => 'MISS'];
$r = simpliroot_cache_purge_run(true);
t('bez cache: brak żądań PURGE', count(array_filter($GLOBALS['http'], function ($x) { return strpos($x, 'PURGE ') === 0; })) === 0);
t('bez cache: still_cached=false', $r['still_cached'] === false);

// 7) czyszczenie po aktualizacji: raz na wersję
$reset();
$cb = $GLOBALS['hooks']['plugins_loaded'][0]; $GLOBALS['hooks']['shutdown'] = [];
$cb();
t('pierwsze uruchomienie wersji: zaplanowane czyszczenie na shutdown', count($GLOBALS['hooks']['shutdown']) === 1 && $GLOBALS['opts']['simpliroot_purged_ver'] === '9.9.9');
$GLOBALS['hooks']['shutdown'] = []; $cb();
t('kolejne uruchomienia tej samej wersji: bez czyszczenia', count($GLOBALS['hooks']['shutdown']) === 0);

// 8) zgodność nazwy z resztą wtyczki
t('simpliroot_purge_all_caches() zwraca raport', is_array(simpliroot_purge_all_caches()));
echo $fail ? "\n$fail FAILED\n" : "\nALL PASSED\n"; exit($fail ? 1 : 0);
