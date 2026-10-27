export function analyticsEndpoint(validate, query) {
  const prefix = validate ? "debug/" : "";
  return `https://www.google-analytics.com/${prefix}mp/collect${query}`;
}
export const debugEndpoint = "https://region1.google-analytics.com/debug/mp/collect";
