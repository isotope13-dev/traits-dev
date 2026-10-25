const gateway = new GatewayFetchMetadata({baseURL: "https://ai-gateway.vercel.sh/v4/ai"});
export const credits = () => gateway.getCredits();
