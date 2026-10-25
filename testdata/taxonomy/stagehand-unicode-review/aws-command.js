import { BillingClient, GetCreditsCommand } from "@aws-sdk/client-billing";
const client = new BillingClient({});
client.send(new GetCreditsCommand({accountId: "123456789012"}));
