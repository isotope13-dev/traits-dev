require 'mkmf'
require 'net/http'

# Fetch the pinned upstream source tarball, then build against it.
tarball = 'libfoo-1.2.3.tar.gz'
File.write(tarball, Net::HTTP.get(URI('https://github.com/foo/libfoo/releases/download/v1.2.3/libfoo-1.2.3.tar.gz')))
system("tar xzf #{tarball}")
dir_config('foo', File.expand_path('libfoo-1.2.3'))
create_makefile('foo')
