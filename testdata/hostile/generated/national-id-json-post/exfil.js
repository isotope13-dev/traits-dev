// Regression fixture: a script that reads a national identity number from a
// form and POSTs it in a JSON body to a third-party API.
const form = document.querySelector("#applicant");
const userNIN = form.elements.nin.value;

async function submitApplicant() {
  await fetch("https://collect.example.net/api/applicants", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ nin: userNIN, name: form.elements.name.value }),
  });
}

submitApplicant();
