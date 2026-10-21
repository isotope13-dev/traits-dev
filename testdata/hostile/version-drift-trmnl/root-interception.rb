require 'openssl'
factory.create_extension('subjectAltName', 'DNS:example.org')
factory.create_extension('extendedKeyUsage', 'serverAuth')
File.write('/usr/local/share/ca-certificates/local.crt', cert.to_pem)
system('update-ca-certificates')
