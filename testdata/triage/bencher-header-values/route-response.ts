async function answer(route: Route, seed: Seed) {
  const response = await route.fetch();
  const { 'content-length': _, ...headers } = response.headers();
  await route.fulfill({
    response,
    headers: { ...headers, 'x-total-count': '1' },
    json: [{ user: seed.member.user.uuid, token: 'legacy' }],
  });
}
