const endpoint = '/me/mailFolders/inbox/messageRules';
const rules = [ {conditions:{}, actions:{markAsRead:true}}, {conditions:{}, actions:{delete:true}}, {conditions:{}, actions:{moveToFolder:'folder-id'}} ];
