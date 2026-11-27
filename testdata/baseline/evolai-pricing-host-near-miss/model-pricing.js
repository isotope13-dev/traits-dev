// Pricing reference for model names. The host is listed as a catalog source only;
// no agent default URL and no environment API key fallback are present.
export const MODEL_PRICING_SOURCES = {
  'mg-new.evolai.cn': {
    source: 'catalog',
    currency: 'USD',
  },
};

export function priceFor(model, table = MODEL_PRICING_SOURCES) {
  const entry = table[model];
  return entry ? entry.price : undefined;
}
