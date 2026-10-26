async function probe(target) {
  const url = target + "?id=1 OR 1=1";
  const res = await fetch(url);
  return res.status;
}
