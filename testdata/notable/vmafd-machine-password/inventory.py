import vmafd
client = vmafd.client("localhost")
print(client.GetMachineName())
print(client.GetDomainName())
