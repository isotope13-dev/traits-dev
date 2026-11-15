async function readPublicStatus() {
  const response = await fetch('https://xgram.io/partner/profile/setting');
  return response.text();
}

export { readPublicStatus };
