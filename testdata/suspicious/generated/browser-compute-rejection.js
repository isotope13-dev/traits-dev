
(function(){
if(navigator.webdriver||window.callPhantom)return!1;
var begun=performance.now();for(var i=0;i<1e5;i++)Math.sqrt(i);if(performance.now()-begun<0.5)return!1;
return!0;
})();
