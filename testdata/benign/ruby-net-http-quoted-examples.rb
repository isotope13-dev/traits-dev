# These API examples are data, not calls. No method below is invoked.
def request_examples
  ["Net::HTTP.post(uri, body)", "Net::HTTP.get(uri)", "Net::HTTP.new(host)",
   "Net::HTTP.put(uri, body)", "Net::HTTP.request(request)"]
end

def unrelated_post(local_store)
  local_store.post("public status")
end
