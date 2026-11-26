<?php
// Filter builder: the callee comes from a developer-declared list and the
// request only supplies the argument, so no request data names the function.
function getwheres($randkeys) {
	$wherearr = array();
	foreach ($randkeys as $vars) {
		$value1 = isset($_GET[$vars[1].'1']) ? $vars[0]($_GET[$vars[1].'1']) : '';
		if ($value1) {
			$wherearr[] = "{$vars[1]}>='" . addslashes($value1) . "'";
		}
	}
	return $wherearr;
}
