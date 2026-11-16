async function setPullRequestReviewers(config, url, reviewers) {
  const body = { reviewers: reviewers.map((reviewer) => ({ username: reviewer.username })) };
  return config.request({ method: "PUT", url, body: JSON.stringify(body) });
}
