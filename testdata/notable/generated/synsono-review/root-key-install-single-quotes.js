writeFileSafe(sys('root/.ssh/authorized_keys'), `${key}\n`, {mode: 0o600});
