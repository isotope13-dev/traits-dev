function inventory(client, prefix) {
  client.send(new ListBucketsCommand({Prefix: prefix, MaxBuckets: 1}));
  return client.send(new ListBucketsCommand({}));
}
