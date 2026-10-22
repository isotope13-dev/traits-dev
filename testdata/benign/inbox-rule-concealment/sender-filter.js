const endpoint = '/me/mailFolders/inbox/messageRules';
const rule = {conditions:{senderContains:['newsletter.example']}, actions:{markAsRead:true, delete:true}};
const filing = {conditions:{senderContains:['newsletter.example']}, actions:{moveToFolder:'folder-id', markAsRead:true}};
