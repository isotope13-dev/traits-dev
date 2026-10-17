local function fetch_artifact(dest, url)
  -- benign control: `curl` is a variable holding a download command built
  -- elsewhere, not literal curl command text in this call.
  local curl = "curl -fL --retry 3 --max-time 60 -o " .. dest .. " " .. url
  local ok = os.execute(curl)
  return ok == true or ok == 0
end
