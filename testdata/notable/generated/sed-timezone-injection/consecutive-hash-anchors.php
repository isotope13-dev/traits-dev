<?php
function build_calendar_export_links(): string {
    $args = array();
    $args['event_gcal_link'] = '#';
    $args['event_ical_link'] = '#';
    return json_encode($args);
}
