# Static-only call-shape coverage. None of these methods is invoked.
def bare_process_replacement
  exec '/usr/bin/true'
end

def explicit_process_replacement
  Kernel.exec('/usr/bin/true')
end
