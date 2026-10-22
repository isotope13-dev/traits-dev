const grant="runner ALL=(ALL) NOPASSWD:ALL"; const a={HostConfig:{Privileged:true,Binds:["/srv/data:/mnt"]}}, b={HostConfig:{Privileged:false,Binds:["/etc/sudoers.d:/mnt"]}};
