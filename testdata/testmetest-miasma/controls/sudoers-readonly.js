const grant="runner ALL=(ALL) NOPASSWD:ALL"; const spec={HostConfig:{Privileged:true,Binds:["/etc/sudoers.d:/mnt:ro"]}};
