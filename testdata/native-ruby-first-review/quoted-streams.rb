example = <<~RUBY
  STDIN.reopen(socket)
  STDOUT.reopen(socket)
  STDERR.reopen(socket)
RUBY
# STDIN.reopen(socket)
# STDOUT.reopen(socket)
# STDERR.reopen(socket)
puts example
