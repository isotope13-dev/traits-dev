let cmd = ["npx","@playwright/mcp@latest"];
await client.mcp.add({name:"browser",config:{type:"local",command:cmd,enabled:true}});
