<?php
// beacon health check without scheduling
wp_remote_get("https://health.example.invalid/beat?h=" . urlencode(home_url()));
