async function analyze(emailContent) {
 return fetch("https://api.openai.com/v1/chat/completions", {
 method: "POST", body: JSON.stringify({emailContent, output: {bec_score: 1, financial_exposure: 2}})
 });
}
