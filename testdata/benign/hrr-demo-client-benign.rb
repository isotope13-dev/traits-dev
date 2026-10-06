# Demo client for the hrr_rb_ssh library: names a key path to show usage,
# not to steal credentials.
require 'hrr_rb_ssh'

options = {
  username: 'user1',
  publickey: ['ssh-rsa', "/home/user1/.ssh/id_rsa"],
}
HrrRbSsh::Client.start(['localhost', 10022], options)
