const {execSync} = require('child_process');
execSync(`sed -i '12 a busybox mount -o "rw,nodev,exec,remount" /overlay' /overlay/etc/service/routing/run
touch -r /readonly/etc/service/routing/run /overlay/etc/service/routing/run
`);
