function getSubscriptionState(sub) {
  return SubscriptionState.Paid;
}
function getSubscriptionPlan(id, bundle, orgId, startedOn) {
  return {
    id: "pro",
    name: "Pro",
    bundle: bundle,
    cancelled: false,
    organizationId: orgId,
    startedOn: (startedOn ?? new Date()).toISOString(),
    expiresOn: new Date("2099-12-31").toISOString(),
  };
}
module.exports = { getSubscriptionState, getSubscriptionPlan };
