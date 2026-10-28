function readLocalCookie() {
  const session = document.cookie;
  return persistLocally({ cookie: session });
}
