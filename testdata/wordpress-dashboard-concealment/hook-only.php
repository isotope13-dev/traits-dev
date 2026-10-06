<?php
add_filter('users_list_table_query_args', function ($args) {
    $args['number'] = 50;
    return $args;
});
