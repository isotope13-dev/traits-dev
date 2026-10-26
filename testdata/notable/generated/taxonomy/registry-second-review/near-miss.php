<?php
$x=array(1=>$site);
$y=$fields['name'];
file_put_contents($base.'/settings.json','{}');
add_action('init','refresh_layout');
function_exists('known_callback');
