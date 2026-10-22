const endpoint = '/me/mailFolders/inbox/messageRules';
const rule = {conditions:{}, actions:{markAsRead:true, delete:true}, isEnabled:false};
const filing = {isEnabled:false, conditions:{}, actions:{markAsRead:true, moveToFolder:'folder-id'}};
