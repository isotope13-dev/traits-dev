#!/bin/sh
payload="20"
curl --data-urlencode 'name=preview_graphs_per_page' --data-urlencode "value=$payload" "$TARGET/auth_profile.php?action=update_data&tab=general"
curl "$TARGET/graph_view.php?action=preview&clear=1"
curl "$TARGET/graph_realtime.php?action=init&local_graph_id=7"
