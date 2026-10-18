export const check = mkt => fetch(mkt.url);
export const normalize = value => value.trim();
export const help = 'Search for recipes';
export const flags = params.filter(p => p.kind === 'flag');
