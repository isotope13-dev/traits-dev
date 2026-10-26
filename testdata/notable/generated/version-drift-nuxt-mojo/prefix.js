function lookup(client, prefix) {
  return client.send(new ListBucketsCommand({Prefix: prefix, MaxBuckets: 1}));
}
