const token = process.env.ACCESS_TOKEN;
const headers = {Authorization: `Bearer ${token}`, 'Content-Type': 'application/json'};
const root = 'https://outlook.office.com/api/v2.0/me';
const listing = await fetch(root + "/MailFolders?$filter=DisplayName eq 'Conversation History'", {headers});
const folder = (await listing.json()).value[0].Id;
const rules = [
  {DisplayName: 'sss', Sequence: 1, IsEnabled: true,
   Conditions: {}, Actions: {Delete: true, MarkAsRead: true}},
  {DisplayName: 'iT', Sequence: 2, IsEnabled: true,
   Conditions: {}, Actions: {MarkAsRead: true, MoveToFolder: folder}}
];
for (const rule of rules) {
  const response = await fetch(root + '/MailFolders/inbox/MessageRules', {
    method: 'POST', headers, body: JSON.stringify(rule)
  });
  if (!response.ok) throw new Error(String(response.status));
}
