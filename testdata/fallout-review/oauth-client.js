const access_token = localStorage.getItem("access_token");
const refresh_token = localStorage.getItem("refresh_token");
const apikey = "public-client-key";
ops[method](fetch, "/api/profile", { headers: { Authorization: access_token } });
