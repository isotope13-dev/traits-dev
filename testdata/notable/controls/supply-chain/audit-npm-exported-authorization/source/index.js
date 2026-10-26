async function operate() {
  const token = process.env.API_TOKEN;
  await fetch("https://service.example.invalid/status", {headers: {Authorization: "Bearer " + token}});
}
module.exports = {operate};
