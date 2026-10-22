const endpoint = '/me/mailFolders/inbox/messageRules';
const ordinary = {conditions:{}, actions:{markAsRead:true}};
const filtered = {conditions:{senderContains:['newsletter.example']}, actions:{markAsRead:true, delete:true, moveToFolder:'folder-id'}};
