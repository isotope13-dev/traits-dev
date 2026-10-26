const res = await fetch("https://raw.githubusercontent.com/acme/acme/main/follow.json");
const ids = await res.json();
await newsletterFollow(ids[0]);
