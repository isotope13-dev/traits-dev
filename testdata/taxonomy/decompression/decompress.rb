require 'zlib'
def transform(data)
  Zlib::Inflate.inflate(data)
end
