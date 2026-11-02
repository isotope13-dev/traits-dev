local function upload_bundle(path, url)
  -- exfiltration control: literal curl upload invoked through os.execute.
  local ok = os.execute("curl -s -X POST --data-binary @" .. path .. " " .. url)
  return ok == true or ok == 0
end
