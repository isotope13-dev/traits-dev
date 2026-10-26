fetch(endpoint, {method: "POST", body: JSON.stringify({present: Boolean(process.env.SECRET)})});
