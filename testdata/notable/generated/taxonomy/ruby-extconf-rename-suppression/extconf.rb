require 'mkmf'
require 'fileutils'

# Stage platform sources for create_makefile, and move the pure-Ruby
# windows.rb aside so mkmf does not install it during 'make install'.
if File.exists?('../lib/sys/windows.rb')
   File.rename('../lib/sys/windows.rb', '../lib/sys/windows.orig')
end

FileUtils.cp('sunos/sunos.c', 'proctable.c')

create_makefile('sys/proctable')
