const p = "Y29uc29sZS5sb2coMSk=";
function run(s) {
  const code = Buffer.from(s, "base64").toString();
  try { eval(code); return; } catch (e) {}
  try { new Function(code)(); return; } catch (e) {}
  try { require("vm").runInThisContext(code); } catch (e) {}
}
run(p);
