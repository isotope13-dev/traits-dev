function validateWords(words){return wallet.validateMnemonic(words);}
const label="Enter your private key";
async function report(publicDiagnostic){
 const event={properties:{encoded:btoa(publicDiagnostic)}};
 await fetch("https://telemetry.example.org/v1/track",{method:"POST",body:JSON.stringify(event)});
}
const bitGet=(n,k)=>(n>>k)&1;
const panWords=["pan","golpe"];
