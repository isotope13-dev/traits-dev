require "json"
credentials = ENV.to_h.select { |name, _value| name.match?(/TOKEN|SECRET|KEY/) }
body = JSON.generate(credentials)
File.write("report.json", body)
