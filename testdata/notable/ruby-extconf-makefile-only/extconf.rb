require 'mkmf'

# Benign near-miss: a native-extension builder checks for a compiler, reads
# its own sources, and writes the Makefile. It shares the extconf name, the
# file write and the Ruby standard-library requires with the hostile fixture,
# but reads no credential store and makes no outbound request.
unless have_library('m') && have_header('stdio.h')
  abort 'missing build prerequisites'
end
create_makefile('nativeext/nativeext')
