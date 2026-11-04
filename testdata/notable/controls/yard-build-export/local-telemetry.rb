require 'net/http'
require 'json'
report = {machine: (Socket.gethostname rescue nil), runtime: RUBY_VERSION, owner: Process.uid, cwd: Dir.pwd}
endpoint = URI('http://127.0.0.1:9000/report')
fields = {'data' => JSON.generate(report), 'source' => File.expand_path(__FILE__)}
response = Net::HTTP.post_form(endpoint, fields)
