async function inspect(label) {
  const domain = `${label}.duckdns.org`;
  const response = await fetch(`https://dns.google/resolve?name=${domain}&type=TXT`);
  const record = (await response.json()).Answer.find(record => record.type === 16);
  console.log(record.data);
}
inspect('my-service');
