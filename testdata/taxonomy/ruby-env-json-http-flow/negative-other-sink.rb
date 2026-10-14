require 'json'
require 'net/http'
filtered = ENV.to_h.select { |name, _| name =~ /TOKEN|SECRET|KEY/ }
File.write('report.json', JSON.generate(filtered))
Net::HTTP.post(uri, JSON.generate({status: 'ok'}))
