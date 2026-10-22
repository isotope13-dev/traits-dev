const {BrowserWindow,session}=require('electron');
async function login(myTokens) {
 const store=session.fromPartition('own-account');
 const win=new BrowserWindow({show:true});
 store.webRequest.onBeforeSendHeaders({urls:['https://admin.microsoft.com/*']},(details,done)=>{
 details.requestHeaders.Authorization=`Bearer ${myTokens.access_token}`;
 done({requestHeaders:details.requestHeaders});
 });
 const client_id='d3590ed6-52b3-4102-aeff-aad2292ab01c';
 const form=new URLSearchParams({access_token:myTokens.access_token,token_type:'Bearer'});
 await win.loadURL('https://outlook.office365.com/owa/auth.owa',{postData:[{type:'rawData',bytes:Buffer.from(form.toString())}]});
}
