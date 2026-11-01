# Blockchain RPC directory review

The HTTP URL RPC leaf held 84 rules and mixed provider identities, blockchain method or field observations, and JMX query paths. Provider-specific endpoints now live with their respective services in `well-known/`; generic Ethereum, EVM and provider-set observations live in blockchain or network profiles; the JMX paths remain HTTP service paths. The old RPC leaf has been removed and consumers updated.

A set of public endpoints does not by itself establish a failover pool. Likewise, a Blockscout hostname alone does not establish an account transaction query, and nearby `eth_call` and result text do not establish result processing. Names and descriptions now state those observed facts. Protocol-specific request behavior remains under the blockchain client taxonomy.
