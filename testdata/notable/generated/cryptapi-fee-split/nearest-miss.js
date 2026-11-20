async function createPayment(ownAddress, coin, url) {
  const response = await fetch(url, {
    method: 'POST',
    body: JSON.stringify({ address: ownAddress, coin }),
  });
  return response.json();
}
