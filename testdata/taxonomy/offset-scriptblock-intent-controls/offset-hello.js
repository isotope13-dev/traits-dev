const {execFileSync}=require("node:child_process");
const stage=String.raw`$key=1000;$data=@(-913,-886,-895,-884,-899,-955,-921,-883,-884,-888,-883,-884,-968,-961,-896,-899,-892,-892,-889,-961);$code='';for($i=0;$i -lt $data.Length;$i++){$code += [char]([int] $data[ $i ] + $key)};&([scriptblock]::Create($code))`;
execFileSync("powershell.exe",["-NoProfile","-Command",stage]);
