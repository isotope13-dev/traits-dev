// Local diagnostics: counts the cookies visible to the popup, nothing sent.
async function countCookies() {
  const rows = await chrome.cookies.getAll({ domain: "example-shop.test" });
  console.log("cookies visible:", rows.length);
  return rows.length;
}
