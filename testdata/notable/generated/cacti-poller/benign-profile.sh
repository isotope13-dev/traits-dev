#!/bin/bash
curl --data-urlencode 'name=preview_graphs_per_page' --data-urlencode 'value=25' "$C/auth_profile.php?tab=general&action=update_data&header=false"
curl "$C/graph_view.php?action=preview&page=1&clear=1"
curl "$C/graph_realtime.php?action=init&local_graph_id=1"
