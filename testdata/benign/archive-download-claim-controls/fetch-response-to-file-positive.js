const fs=require('fs');
async function downloadPublicArchive() {
  const response=await fetch('https://example.org/public/manual.tar.gz');
  const bytes=Buffer.from(await response.arrayBuffer());
  fs.writeFileSync('/tmp/public-archive.tar.gz',bytes);
}
module.exports={downloadPublicArchive};
