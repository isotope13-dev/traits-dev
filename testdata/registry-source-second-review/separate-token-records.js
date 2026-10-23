export function access(auth) { return { access_token: auth.access_token }; }
export function refresh(auth) { return { refresh_token: auth.refresh_token }; }
const example = "return { access_token: a, refresh_token: r };";
