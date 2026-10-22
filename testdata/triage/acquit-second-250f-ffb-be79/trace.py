"""Trace supplied code in bounded emulators with no host/network effects.

Usage: python3 trace.py EXTRACTED_ROOT OUTER_ELF OUTPUT_JSON
Requires quickjs and unicorn. Only the regional JS snippet and UDP inner loop
are evaluated; callbacks, storage, send operations and timers are all stubbed.
"""
import json
from pathlib import Path
import struct
import sys
import quickjs
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE
from unicorn.x86_const import *

root, elf_path, output = map(Path, sys.argv[1:])
js_results = []
for name in ["sweetalert2.all.min.js", "sweetalert2.mjs"]:
    source = (root / "public/vendor/sweetalert2" / name).read_text()
    start = source.index('if("undefined"!=typeof window&&/^ru')
    end = source.index(".prototype.disableButtons", start)
    # Strip the minified constructor identifier immediately before .prototype.
    end = source.rfind("}", start, end) + 1
    payload = source[start:end]
    for label, language, host, age in [
        ("first visit", "ru-RU", "site.ru", None),
        ("expired", "ru-RU", "site.ru", 4),
        ("threshold", "ru-RU", "site.ru", 3),
        ("other language", "en-US", "site.ru", 4),
        ("other host", "ru-RU", "site.com", 4),
        ("Belarus", "ru", "site.by", 4),
    ]:
        ctx = quickjs.Context()
        ctx.eval("""
          var calls=[], timers=[], queue=[], stored=null;
          var window={}, navigator={}, location={};
          var localStorage={
            getItem: function(k){calls.push("read");return stored},
            setItem: function(k,v){calls.push("write");stored=v}
          };
          var document={body:{style:{},appendChild:function(e){calls.push("append:"+e.src)}},
            createElement:function(t){calls.push("create:"+t);return {
              play:function(){calls.push("play");return {catch:function(){}}}
            }}
          };
          function setTimeout(fn,delay){timers.push(delay);queue.push(fn)}
          var NativeDate=Date;
          var Date=class extends NativeDate {
            constructor(...args){super(...(args.length?args:[1700000000000]))}
            static parse(s){return NativeDate.parse(s)}
          };
        """)
        ctx.eval("navigator.language="+json.dumps(language)+";location.host="+json.dumps(host)+";")
        if age is not None:
            ctx.eval(f"stored=new NativeDate(1700000000000-{age}*86400000).toISOString()")
        ctx.eval(payload)
        ctx.eval("while(queue.length)queue.shift()()")
        observed = json.loads(ctx.eval("""JSON.stringify({
          blocked:document.body.style.pointerEvents==="none",
          plays:calls.includes("play"),initialized:calls.includes("write"),
          calls:calls,timers:timers
        })"""))
        expected = label in {"expired", "Belarus"}
        assert observed["blocked"] == expected, (name, label, observed)
        assert observed["plays"] == expected, (name, label, observed)
        assert observed["initialized"] == (label == "first visit")
        js_results.append({"member":name, "case":label, **observed})

data = elf_path.read_bytes()
assert data[0x3374:0x3378] == bytes.fromhex("74 cb eb e1")
loop_results=[]
for displacement, length in [(0xca,512),(0xcb,512),(0xcb,0),(0xcd,512)]:
    code=bytearray(data);code[0x3375]=displacement
    emu=Uc(UC_ARCH_X86, UC_MODE_64)
    emu.mem_map(0x400000, 0x20000);emu.mem_write(0x400000,bytes(code))
    emu.mem_map(0x200000,0x30000);emu.mem_map(0x700000,0x20000)
    stack=0x710000
    for reg,value in [(UC_X86_REG_RSP,stack),(UC_X86_REG_RBP,length),
                      (UC_X86_REG_R13,2),(UC_X86_REG_R14,0x200000),
                      (UC_X86_REG_R15,0x210000)]:
        emu.reg_write(reg,value)
    emu.mem_write(stack+0x25,b"\x02")
    emu.mem_write(stack+0x2d,b"\0")
    emu.mem_write(0x200000,struct.pack("<II",5,6))
    emu.mem_write(0x210000,struct.pack("<QQ",0x220000,0x221000))
    sends=[]
    def hook(uc,address,size,user):
        if address==0x40b488:
            sends.append({"fd":uc.reg_read(UC_X86_REG_RDI),
                          "length":uc.reg_read(UC_X86_REG_RDX)})
            sp=uc.reg_read(UC_X86_REG_RSP)
            ret=struct.unpack("<Q",uc.mem_read(sp,8))[0]
            uc.reg_write(UC_X86_REG_RSP,sp+8)
            uc.reg_write(UC_X86_REG_RAX,length)
            uc.reg_write(UC_X86_REG_RIP,ret)
            if len(sends)>=6:uc.emu_stop()
    emu.hook_add(UC_HOOK_CODE,hook)
    emu.emu_start(0x403340,0x403378,count=300)
    expected=6 if (displacement==0xca or displacement==0xcb and length>0) else 2
    assert len(sends)==expected,(displacement,length,sends)
    loop_results.append({"branch":hex(displacement),"length":length,
                         "stubbed_sends":len(sends)})
output.write_text(json.dumps({"regional_snippet":js_results,"udp_loop":loop_results},indent=2)+"\n")
print(f"PASS {len(js_results)} regional cases and {len(loop_results)} UDP loop cases")
