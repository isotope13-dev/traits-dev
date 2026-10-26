function selectProvider({providerOrder: order}) {
  return order.filter(provider => provider.enabled);
}
const providerOrder = ["anime", "manga"];
