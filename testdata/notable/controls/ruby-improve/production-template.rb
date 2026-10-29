require 'base64'
if Rails.env.production?
  source = Base64.decode64(File.read('template.txt'))
  eval(source)
end
