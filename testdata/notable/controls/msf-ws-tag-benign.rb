# Framework RPC daemon tags its own websocket listener `msf-ws`: same
# constant shape as the SMA tunnel tag, unrelated protocol. Must not read
# as SMA exploitation.
WS_TAG = 'msf-ws'
WS_CONF = "#{WS_TAG}.pem"
