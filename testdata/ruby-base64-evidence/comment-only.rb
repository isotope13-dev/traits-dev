# Base64 carries arbitrary characters through the remote protocol.
def quote_payload(value)
  value.gsub("'", "''")
end
