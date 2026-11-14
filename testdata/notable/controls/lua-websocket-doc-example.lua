-- Documentation example for a reusable WebSocket client.
-- It shows a private-network endpoint in its usage comment; this module
-- contains no WebSocket command handler or data collection.
-- @usage local ws = websocket.new("ws://192.0.2.44:8080")
local request = "GET / HTTP/1.1\r\nConnection: Upgrade\r\nUpgrade: websocket\r\n"
return request
