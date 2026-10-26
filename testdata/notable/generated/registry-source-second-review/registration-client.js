export const register = data => fetch("https://service.example/register", {method: "POST", body: JSON.stringify(data)});
