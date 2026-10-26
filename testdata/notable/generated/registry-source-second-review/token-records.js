export function tokens(auth) {
  return { refresh_token: auth.refresh_token, access_token: auth.access_token };
}
