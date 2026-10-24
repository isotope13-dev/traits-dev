fetch(service + "/extension/analyze", {
  method: "POST", body: JSON.stringify({secret_value: token})
});
