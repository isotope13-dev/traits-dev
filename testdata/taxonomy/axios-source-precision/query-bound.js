const params = new URLSearchParams(location.search);
params.forEach((value, key) => consume(key, value));
