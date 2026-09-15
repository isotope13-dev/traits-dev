#!/usr/bin/env python3
"""Generate package-shaped, inert supply-chain detection fixtures."""

from __future__ import annotations

import base64
import gzip
import hashlib
import io
import json
import os
import shlex
import shutil
import subprocess
import struct
import tarfile
import tempfile
import textwrap
import zipfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "testdata" / "hostile" / "supply-chain-benchmark-v1"
FIXED_TIME = 1_700_000_000
ZW = "\u2063"


@dataclass(frozen=True)
class Language:
    key: str
    ecosystem: str
    extension: str
    artifact: str


@dataclass(frozen=True)
class Scenario:
    key: str
    platform: str
    concealment: str
    objective: str
    action: str

    @property
    def hidden(self) -> bool:
        return self.concealment != "plain"


LANGUAGES = (
    Language("python", "pypi", "py", "tar.gz"),
    Language("javascript", "npm", "js", "tgz"),
    Language("typescript", "npm", "ts", "tgz"),
    Language("go", "gomod", "go", "zip"),
    Language("rust", "crates", "rs", "crate"),
    Language("ruby", "rubygems", "rb", "gem"),
    Language("php", "packagist", "php", "zip"),
    Language("shell", "debian", "sh", "deb"),
    Language("lua", "luarocks", "lua", "src.rock"),
    Language("perl", "cpan", "pm", "tar.gz"),
    Language("powershell", "psgallery", "psm1", "nupkg"),
    Language("java", "maven", "java", "jar"),
    Language("csharp", "nuget", "cs", "nupkg"),
    Language("c", "conan", "c", "tar.gz"),
    Language("swift", "swiftpm", "swift", "zip"),
    Language("objectivec", "cocoapods", "m", "zip"),
    Language("groovy", "gradle", "groovy", "jar"),
    Language("scala", "sbt", "scala", "jar"),
    Language("kotlin", "gradle", "kt", "jar"),
    Language("zig", "zigmod", "zig", "tar.gz"),
    Language("elixir", "hex", "ex", "tar"),
)


SCENARIOS = (
    Scenario("install-env-report", "linux", "plain", "recon-exfil", "POST /v1/install fields=CI_JOB_TOKEN,NPM_TOKEN,CARGO_REGISTRY_TOKEN"),
    Scenario("cron-cache-refresh", "linux", "plain", "persistence", "WRITE /etc/cron.d/cache-refresh value=@reboot /usr/lib/cache-refresh/agent"),
    Scenario("ssh-rc-fallback", "linux", "zero-width-hex-xor", "persistence", "APPEND ~/.ssh/rc command=/usr/lib/ssh-cache/session-helper"),
    Scenario("png-resource-loader", "linux", "png-trailer-hex-xor", "hidden-payload", "EXEC /bin/sh -c /tmp/.font-cache-update"),
    Scenario("preload-config", "linux", "hex-xor", "hijack-execution-flow", "WRITE /etc/ld.so.preload value=/usr/lib/libcacheaudit.so"),
    Scenario("launchagent-checkin", "macos", "plain", "persistence", "WRITE ~/Library/LaunchAgents/com.cache.telemetry.plist ProgramArguments=/usr/local/lib/cache-agent"),
    Scenario("dyld-build-probe", "macos", "reversed-hex-xor", "hijack-execution-flow", "SET DYLD_INSERT_LIBRARIES=/Library/Caches/.libtelemetry.dylib"),
    Scenario("keychain-helper", "macos", "plain", "credential-access", "EXEC security find-generic-password -ga developer-session"),
    Scenario("loginitem-doc-channel", "macos", "zero-width-hex-xor", "persistence", "EXEC osascript -e tell application System Events to make login item"),
    Scenario("dns-profile-label", "macos", "png-trailer-hex-xor", "recon-exfil", "LOOKUP host.user.arch.edge-cache.example type=TXT"),
    Scenario("runkey-telemetry", "windows", "plain", "persistence", r"REG ADD HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v CacheTelemetry"),
    Scenario("scheduled-token-sync", "windows", "plain", "persistence", r"SCHTASKS /Create /SC ONLOGON /TN CacheTokenSync /TR %LOCALAPPDATA%\CacheSync\agent.exe"),
    Scenario("startup-link-sidecar", "windows", "hex-xor", "persistence", r"WRITE %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\CacheSync.lnk"),
    Scenario("rundll-resource-stage", "windows", "reversed-hex-xor", "hidden-payload", r"EXEC rundll32.exe %TEMP%\cachecodec.dll,TelemetryInit"),
    Scenario("wmi-filter-cache", "windows", "png-trailer-hex-xor", "persistence", "CREATE __EventFilter CommandLineEventConsumer root\\subscription CacheUpdateFilter"),
)


STEMS = (
    "pathweaver", "cacheharbor", "sessioncodec", "fontstream", "nativeledger",
    "configquill", "buildtide", "keyringbridge", "dockwatch", "resolvermesh",
    "profileloom", "taskglider", "shortcutforge", "resourcecove", "eventgrove",
)


def q(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def identity(language: Language, scenario: Scenario, index: int) -> dict[str, str]:
    name = f"{STEMS[index]}-{language.key.replace('objectivec', 'objc')}"
    seed = hashlib.sha256(f"{language.key}:{scenario.key}".encode()).digest()
    gate = "_" + base64.b32encode(seed[:8]).decode().rstrip("=")
    token = base64.urlsafe_b64encode(seed[8:20]).decode().rstrip("=")
    host = f"ingest-{scenario.platform}.{name}.edge.example"
    return {"name": name, "gate": gate, "token": token, "host": host}


def encoded_payload(scenario: Scenario, action: str) -> tuple[str, bool]:
    if scenario.concealment == "plain":
        return action, False
    raw = bytes(b ^ 0x23 for b in action.encode())
    blob = raw.hex()
    reverse = scenario.concealment.startswith("reversed")
    if reverse:
        blob = blob[::-1]
    if scenario.concealment.startswith("zero-width"):
        blob = ZW.join(blob[i : i + 3] for i in range(0, len(blob), 3))
    return blob, reverse


def source_for(language: Language, scenario: Scenario, ident: dict[str, str]) -> str:
    action = scenario.action.replace("cache", ident["name"])
    blob, reverse = encoded_payload(scenario, action)
    carrier = scenario.concealment.startswith("png-trailer")
    hidden = scenario.hidden
    values = {
        "name": ident["name"], "gate": ident["gate"], "token": ident["token"],
        "host": ident["host"], "action": action, "blob": blob,
        "reverse": reverse, "carrier": carrier,
        "hidden": hidden, "platform": scenario.platform,
    }
    source = SOURCE_BUILDERS[language.key](values)
    assert ident["gate"] in source and ident["token"] in source, (language.key, scenario.key, "gate")
    assert ("127.0.0.1" in source or "{127,0,0,1}" in source) and ident["host"] in source, (language.key, scenario.key, "sink")
    if scenario.hidden:
        assert action not in source
    folded = source.replace(" ", "").lower()
    for unsafe in ("system(spec", "exec(spec", "eval(spec", "command::new(&spec", "processbuilder(spec"):
        assert unsafe not in folded, (language.key, scenario.key, unsafe)
    return source


def py_source(v: dict) -> str:
    recover = f"spec = {q(v['action'])}" if not v["hidden"] else textwrap.dedent(f"""
        raw = ({'Path("assets/cache.png").read_bytes().split(b"STEG:", 1)[1].decode()' if v['carrier'] else q(v['blob'])})
        raw = raw.replace("\\u2063", "")
        if {str(v['reverse'])}: raw = raw[::-1]
        spec = bytes(int(raw[i:i+2], 16) ^ 0x23 for i in range(0, len(raw), 2)).decode()
    """).strip()
    return (
        "import os, socket, subprocess, sys, tempfile\n"
        "from pathlib import Path\n"
        "def _prime():\n"
        f"    if os.environ.get({q(v['gate'])}) != {q(v['token'])}: return\n"
        f"{textwrap.indent(recover, '    ')}\n"
        f"    Path(tempfile.gettempdir(), \".{v['name']}.idx\").write_text(spec)\n"
        "    subprocess.run([sys.executable, \"-c\", \"print('index refreshed')\"], stdout=subprocess.DEVNULL)\n"
        "    try:\n"
        "        s=socket.create_connection((\"127.0.0.1\", 9), timeout=.2)\n"
        f"        s.sendall((\"POST /v1/pulse HTTP/1.1\\r\\nHost: {v['host']}\\r\\nContent-Length: 12\\r\\n\\r\\ncache=primed\").encode()); s.close()\n"
        "    except OSError: pass\n"
        "_prime()\n"
    )


def js_source(v: dict, typescript: bool = False) -> str:
    type_bits = ": string" if typescript else ""
    source = "fs.readFileSync(path.join(process.cwd(),'assets','cache.png')).toString().split('STEG:')[1]" if v["carrier"] else q(v["blob"])
    recover = f"let spec{type_bits}={q(v['action'])};" if not v["hidden"] else f"let raw{type_bits}={source}.replace(/\\u2063/g,''); if ({str(v['reverse']).lower()}) raw=[...raw].reverse().join(''); let spec{type_bits}=Buffer.from(raw,'hex').map(x=>x^0x23).toString();"
    return textwrap.dedent(f"""
        const fs=require('fs'),os=require('os'),path=require('path'),net=require('net'),cp=require('child_process');
        function prime(){{
          if(process.env[{q(v['gate'])}]!=={q(v['token'])}) return;
          {recover}
          fs.writeFileSync(path.join(os.tmpdir(),'.{v['name']}.idx'),spec);
          cp.spawnSync(process.execPath,['-e',"process.stdout.write('index refreshed')"],{{stdio:'ignore'}});
          const s=net.createConnection({{host:'127.0.0.1',port:9}}); s.setTimeout(200);
          s.on('connect',()=>s.end('POST /v1/pulse HTTP/1.1\\r\\nHost: {v['host']}\\r\\nContent-Length: 12\\r\\n\\r\\ncache=primed')); s.on('error',()=>{{}}); s.on('timeout',()=>s.destroy());
        }}
        prime();
    """).lstrip()


def go_source(v: dict) -> str:
    source = 'string(must(os.ReadFile(filepath.Join(filepath.Dir(sourceFile()), "assets", "cache.png"))))' if v["carrier"] else q(v["blob"])
    recover = f"spec := {q(v['action'])}" if not v["hidden"] else f"raw := strings.Split({source}, \"STEG:\")[len(strings.Split({source}, \"STEG:\"))-1]; raw = strings.ReplaceAll(raw, \"\\u2063\", \"\"); if {str(v['reverse']).lower()} {{ r:=[]rune(raw); for i,j:=0,len(r)-1;i<j;i,j=i+1,j-1 {{ r[i],r[j]=r[j],r[i] }}; raw=string(r) }}; b,_:=hex.DecodeString(raw); for i:=range b {{ b[i]^=0x23 }}; spec:=string(b)"
    return textwrap.dedent(f"""
        package {v['name'].replace('-', '')}
        import("encoding/hex";"net";"os";"os/exec";"path/filepath";"runtime";"strings";"time")
        func must(b []byte,e error)[]byte{{return b}}
        func sourceFile()string{{_,f,_,_:=runtime.Caller(0);return f}}
        func init(){{if os.Getenv({q(v['gate'])})!={q(v['token'])}{{return}}; {recover}; _=os.WriteFile(filepath.Join(os.TempDir(),".{v['name']}.idx"),[]byte(spec),0600); _=exec.Command({q('cmd' if v['platform']=='windows' else 'sh')},{q('/c' if v['platform']=='windows' else '-c')},{q('echo index refreshed' if v['platform']=='windows' else ':')}).Run(); c,e:=net.DialTimeout("tcp","127.0.0.1:9",200*time.Millisecond);if e==nil{{c.Write([]byte("POST /v1/pulse HTTP/1.1\\r\\nHost: {v['host']}\\r\\n\\r\\n"));c.Close()}}}}
    """).lstrip()


def rust_source(v: dict) -> str:
    source = 'std::fs::read_to_string("assets/cache.png").unwrap_or_default().split("STEG:").last().unwrap_or("").to_string()' if v["carrier"] else f"{q(v['blob'])}.to_string()"
    recover = f"let spec={q(v['action'])}.to_string();" if not v["hidden"] else f"let mut raw={source}.replace('\\u{{2063}}',\"\"); if {str(v['reverse']).lower()} {{raw=raw.chars().rev().collect();}} let spec=(0..raw.len()).step_by(2).map(|i|u8::from_str_radix(&raw[i..i+2],16).unwrap_or(0)^0x23).map(char::from).collect::<String>();"
    return textwrap.dedent(f"""
        use std::{{env,fs,io::Write,net::TcpStream,process::Command,time::Duration}};
        fn main(){{if env::var({q(v['gate'])}).ok().as_deref()!=Some({q(v['token'])}){{return}} {recover} let mut p=env::temp_dir();p.push(".{v['name']}.idx");let _=fs::write(p,spec);let _=Command::new(if cfg!(windows){{"cmd"}}else{{"printf"}}).args(if cfg!(windows){{vec!["/c","echo index refreshed"]}}else{{vec!["index refreshed"]}}).output();if let Ok(mut s)=TcpStream::connect_timeout(&"127.0.0.1:9".parse().unwrap(),Duration::from_millis(200)){{let _=s.write_all(b"POST /v1/pulse HTTP/1.1\r\nHost: {v['host']}\r\n\r\n");}}}}
    """).lstrip()


def ruby_source(v: dict) -> str:
    source = "File.binread(File.join(Dir.pwd,'assets','cache.png')).split('STEG:').last" if v["carrier"] else q(v["blob"])
    recover = f"spec={q(v['action'])}" if not v["hidden"] else f"raw={source}.delete(\"\\u2063\");raw=raw.reverse if {str(v['reverse']).lower()};spec=[raw].pack('H*').bytes.map{{|b|(b^0x23).chr}}.join"
    return textwrap.dedent(f"""
        require 'socket';require 'tmpdir';require 'rbconfig'
        if ENV[{q(v['gate'])}]=={q(v['token'])}
          {recover};File.write(File.join(Dir.tmpdir,'.{v['name']}.idx'),spec);system(RbConfig.ruby,'-e',"print 'index refreshed'",out:File::NULL)
          begin;s=Socket.tcp('127.0.0.1',9,connect_timeout:0.2);s.write("POST /v1/pulse HTTP/1.1\r\nHost: {v['host']}\r\n\r\n");s.close;rescue;end
        end
    """).lstrip()


def php_source(v: dict) -> str:
    source = "explode('STEG:',file_get_contents(__DIR__.'/assets/cache.png'))[1]" if v["carrier"] else q(v["blob"])
    recover = f"$spec={q(v['action'])};" if not v["hidden"] else f"$raw=str_replace(\"\\u{{2063}}\",'',{source});if({str(v['reverse']).lower()})$raw=strrev($raw);$b=hex2bin($raw);$spec='';for($i=0;$i<strlen($b);$i++)$spec.=chr(ord($b[$i])^0x23);"
    return textwrap.dedent(f"""
        <?php
        if(getenv({q(v['gate'])})!=={q(v['token'])})return;{recover}
        file_put_contents(sys_get_temp_dir().'/.{v['name']}.idx',$spec);proc_close(proc_open(PHP_BINARY.' -r '.escapeshellarg("print 'index refreshed';"),array(),$pipes));
        $s=@fsockopen('127.0.0.1',9,$e,$m,0.2);if($s){{fwrite($s,"POST /v1/pulse HTTP/1.1\r\nHost: {v['host']}\r\n\r\n");fclose($s);}}
    """).lstrip()


def shell_source(v: dict) -> str:
    if not v["hidden"]:
        recover = f"spec={shlex.quote(v['action'])}"
    else:
        source = "$(sed -n 's/.*STEG://p' \"$(dirname \"$0\")/assets/cache.png\")" if v["carrier"] else shlex.quote(v["blob"])
        reverse_step = 'raw=$(printf %s "$raw" | rev);' if v["reverse"] else ""
        recover = f"raw={source}; raw=$(printf %s \"$raw\" | tr -d '\u2063'); {reverse_step} spec=$(printf %s \"$raw\" | xxd -r -p | perl -pe 's/(.)/chr(ord($1)^0x23)/ges')"
    return textwrap.dedent(f"""
        #!/bin/sh
        [ "$(printenv {shlex.quote(v['gate'])})" = {shlex.quote(v['token'])} ] || exit 0
        {recover}
        printf %s "$spec" > "${{TMPDIR:-/tmp}}/.{v['name']}.idx"
        /bin/sh -c ':' >/dev/null 2>&1
        curl --silent --max-time 1 http://127.0.0.1:9/v1/pulse -H {shlex.quote('Host: '+v['host'])} --data 'cache=primed' >/dev/null 2>&1 || true
    """).lstrip()


def lua_source(v: dict) -> str:
    source = "assert(io.open((debug.getinfo(1).source:sub(2):match('(.*[/\\\\])') or '')..'assets/cache.png','rb')):read('*a'):match('STEG:(.+)')" if v["carrier"] else q(v["blob"])
    recover = f"local spec={q(v['action'])}" if not v["hidden"] else f"local raw=({source}):gsub('\\226\\129\\163','');if {str(v['reverse']).lower()} then raw=raw:reverse() end;local t={{}};for i=1,#raw,2 do t[#t+1]=string.char((tonumber(raw:sub(i,i+1),16)~0x23)) end;local spec=table.concat(t)"
    return textwrap.dedent(f"""
        local socket=require('socket');if os.getenv({q(v['gate'])})~={q(v['token'])} then return end
        {recover};local p=(os.getenv('TMPDIR') or os.getenv('TEMP') or '/tmp')..'/.{v['name']}.idx';local f=assert(io.open(p,'wb'));f:write(spec);f:close();os.execute("printf 'index refreshed' >/dev/null")
        local s=socket.tcp();s:settimeout(0.2);if s:connect('127.0.0.1',9) then s:send('POST /v1/pulse HTTP/1.1\\r\\nHost: {v['host']}\\r\\n\\r\\n');s:close() end
    """).lstrip()


def perl_source(v: dict) -> str:
    source = "do{local $/;open my $f,'<','assets/cache.png';my $x=<$f>;$x=~/STEG:(.+)/s;$1}" if v["carrier"] else q(v["blob"])
    recover = f"my $spec={q(v['action'])};" if not v["hidden"] else f"my $raw={source};$raw=~s/\\x{{2063}}//g;$raw=reverse($raw) if {1 if v['reverse'] else 0};my $bytes=pack('H*',$raw);my $spec=join('',map{{chr(ord($_)^0x23)}}split//,$bytes);"
    return textwrap.dedent(f"""
        package Cache::Prime;use strict;use warnings;use IO::Socket::INET;use File::Spec;
        if(($ENV{{{v['gate']}}}//'') eq {q(v['token'])}){{{recover}open my $o,'>',File::Spec->catfile(File::Spec->tmpdir,'.{v['name']}.idx');print $o $spec;close $o;system($^X,'-e',"print 'index refreshed'");my $s=IO::Socket::INET->new(PeerAddr=>'127.0.0.1',PeerPort=>9,Timeout=>1);print $s "POST /v1/pulse HTTP/1.1\r\nHost: {v['host']}\r\n\r\n" if $s;close $s if $s;}}1;
    """).lstrip()


def powershell_source(v: dict) -> str:
    source = "([IO.File]::ReadAllText((Join-Path $PSScriptRoot 'assets/cache.png')) -split 'STEG:')[-1]" if v["carrier"] else q(v["blob"])
    recover = f"$spec={q(v['action'])}" if not v["hidden"] else f"$raw=({source}).Replace([char]0x2063,'');if(${str(v['reverse']).lower()}){{$raw=-join $raw[$raw.Length..0]}};$b=for($i=0;$i-lt$raw.Length;$i+=2){{[Convert]::ToByte($raw.Substring($i,2),16)-bxor 0x23}};$spec=[Text.Encoding]::UTF8.GetString($b)"
    return textwrap.dedent(f"""
        $gate=[Environment]::GetEnvironmentVariable({q(v['gate'])});if($gate-ne{q(v['token'])}){{return}};{recover}
        [IO.File]::WriteAllText((Join-Path ([IO.Path]::GetTempPath()) '.{v['name']}.idx'),$spec);Start-Process $PSHOME/pwsh -ArgumentList '-NoProfile','-Command','Write-Output index-refreshed' -WindowStyle Hidden -Wait
        try{{$c=[Net.Sockets.TcpClient]::new();$c.Connect('127.0.0.1',9);$w=[IO.StreamWriter]::new($c.GetStream());$w.Write("POST /v1/pulse HTTP/1.1`r`nHost: {v['host']}`r`n`r`n");$w.Dispose();$c.Dispose()}}catch{{}}
    """).lstrip()


def java_like_source(v: dict, language: str) -> str:
    source = 'Files.readString(Path.of("assets/cache.png")).split("STEG:")[1]' if v["carrier"] else q(v["blob"])
    if language == "java":
        recover = f"String spec={q(v['action'])};" if not v["hidden"] else f"String raw={source}.replace(\"\\u2063\",\"\");if({str(v['reverse']).lower()})raw=new StringBuilder(raw).reverse().toString();byte[] b=new byte[raw.length()/2];for(int i=0;i<b.length;i++)b[i]=(byte)(Integer.parseInt(raw.substring(i*2,i*2+2),16)^0x23);String spec=new String(b,StandardCharsets.UTF_8);"
        return textwrap.dedent(f"""
            package edge.cache;import java.io.*;import java.net.*;import java.nio.charset.*;import java.nio.file.*;
            public final class Bootstrap{{static{{if({q(v['token'])}.equals(System.getenv({q(v['gate'])}))){{try{{{recover}Files.writeString(Path.of(System.getProperty("java.io.tmpdir"),".{v['name']}.idx"),spec);new ProcessBuilder(System.getProperty("java.home")+"/bin/java","-version").start().waitFor();try(Socket s=new Socket()){{s.connect(new InetSocketAddress("127.0.0.1",9),200);s.getOutputStream().write("POST /v1/pulse HTTP/1.1\\r\\nHost: {v['host']}\\r\\n\\r\\n".getBytes());}}}}catch(Exception ignored){{}}}}}}}}
        """).lstrip()
    if language == "groovy":
        recover = f"def spec={q(v['action'])}" if not v["hidden"] else f"def raw=({source}).replace('\\u2063','');if({str(v['reverse']).lower()})raw=raw.reverse();def spec=raw.decodeHex().collect{{(it^0x23) as byte}} as byte[];spec=new String(spec,'UTF-8')"
        return f"import java.nio.file.*;import java.net.*\nif(System.getenv({q(v['gate'])})!={q(v['token'])})return\n{recover}\nFiles.writeString(Path.of(System.getProperty('java.io.tmpdir'),'.{v['name']}.idx'),spec);new ProcessBuilder('java','-version').start().waitFor();try{{def s=new Socket('127.0.0.1',9);s.outputStream<<'Host: {v['host']}\\r\\n\\r\\n';s.close()}}catch(Exception ignored){{}}\n"
    if language == "scala":
        recover = f"val spec={q(v['action'])}" if not v["hidden"] else f"var raw=({source}).replace(\"\\u2063\",\"\");if({str(v['reverse']).lower()})raw=raw.reverse;val spec=raw.grouped(2).map(x=>(Integer.parseInt(x,16)^0x23).toChar).mkString"
        return f"package edge.cache\nimport java.nio.file.{{Files,Path}};import java.net.Socket\nobject Bootstrap extends App{{if(sys.env.get({q(v['gate'])}).contains({q(v['token'])})){{{recover};Files.writeString(Path.of(System.getProperty(\"java.io.tmpdir\"),\".{v['name']}.idx\"),spec);new ProcessBuilder(\"java\",\"-version\").start.waitFor;try{{val s=new Socket(\"127.0.0.1\",9);s.getOutputStream.write(\"Host: {v['host']}\\r\\n\\r\\n\".getBytes);s.close}}catch{{case _:Exception=>}}}}}}\n"
    recover = f"val spec={q(v['action'])}" if not v["hidden"] else f"var raw=({source}).replace(\"\\u2063\",\"\");if({str(v['reverse']).lower()})raw=raw.reversed();val spec=raw.chunked(2).map{{(it.toInt(16) xor 0x23).toChar()}}.joinToString(\"\")"
    return f"package edge.cache\nimport java.nio.file.*;import java.net.Socket\nobject Bootstrap{{init{{if(System.getenv({q(v['gate'])})=={q(v['token'])}){{{recover};Files.writeString(Path.of(System.getProperty(\"java.io.tmpdir\"),\".{v['name']}.idx\"),spec);ProcessBuilder(\"java\",\"-version\").start().waitFor();try{{Socket(\"127.0.0.1\",9).use{{it.getOutputStream().write(\"Host: {v['host']}\\r\\n\\r\\n\".toByteArray())}}}}catch(_:Exception){{}}}}}}}}\n"


def csharp_source(v: dict) -> str:
    source = 'File.ReadAllText(Path.Combine(AppContext.BaseDirectory,"assets","cache.png")).Split("STEG:")[1]' if v["carrier"] else q(v["blob"])
    recover = f"var spec={q(v['action'])};" if not v["hidden"] else f"var raw={source}.Replace(\"\\u2063\",\"\");if({str(v['reverse']).lower()})raw=new string(raw.Reverse().ToArray());var b=Enumerable.Range(0,raw.Length/2).Select(i=>(byte)(Convert.ToByte(raw.Substring(i*2,2),16)^0x23)).ToArray();var spec=Encoding.UTF8.GetString(b);"
    return textwrap.dedent(f"""
        using System;using System.IO;using System.Linq;using System.Net.Sockets;using System.Diagnostics;using System.Runtime.CompilerServices;using System.Text;
        internal static class Bootstrap{{[ModuleInitializer]internal static void Init(){{if(Environment.GetEnvironmentVariable({q(v['gate'])})!={q(v['token'])})return;{recover}File.WriteAllText(Path.Combine(Path.GetTempPath(),".{v['name']}.idx"),spec);Process.Start(new ProcessStartInfo({q('cmd.exe' if v['platform']=='windows' else '/usr/bin/printf')},{q('/c echo index refreshed' if v['platform']=='windows' else 'index refreshed')}){{UseShellExecute=false,CreateNoWindow=true}})?.WaitForExit();try{{using var c=new TcpClient();c.Connect("127.0.0.1",9);var b2=Encoding.ASCII.GetBytes("Host: {v['host']}\\r\\n\\r\\n");c.GetStream().Write(b2);}}catch{{}}}}}}
    """).lstrip()


def c_source(v: dict) -> str:
    source = q(v["blob"].replace(ZW, "") if not v["carrier"] else encoded_payload(Scenario("x","x","hex-xor","x",v["action"]), v["action"])[0])
    if not v["hidden"]:
        recover = f"const char *spec={q(v['action'])};"
    else:
        recover = f"char *raw=strdup({source});if({1 if v['reverse'] else 0}){{for(size_t i=0,j=strlen(raw)-1;i<j;i++,j--){{char t=raw[i];raw[i]=raw[j];raw[j]=t;}}}}size_t n=strlen(raw)/2;char *spec=calloc(n+1,1);for(size_t i=0;i<n;i++){{unsigned x=0;sscanf(raw+i*2,\"%2x\",&x);spec[i]=(char)(x^0x23);}}"
    return textwrap.dedent(f"""
        #include <stdio.h>
        #include <stdlib.h>
        #include <string.h>
        #ifdef _WIN32
        #include <winsock2.h>
        #else
        #include <arpa/inet.h>
        #include <sys/socket.h>
        #include <unistd.h>
        #endif
        __attribute__((constructor)) static void prime(void){{const char*g=getenv({q(v['gate'])});if(!g||strcmp(g,{q(v['token'])}))return;{recover}char p[512];snprintf(p,sizeof p,"%s/.{v['name']}.idx",getenv("TMPDIR")?getenv("TMPDIR"):"/tmp");FILE*f=fopen(p,"wb");if(f){{fwrite(spec,1,strlen(spec),f);fclose(f);}}system("printf 'index refreshed' >/dev/null");int s=socket(AF_INET,SOCK_STREAM,0);struct sockaddr_in a={{.sin_family=AF_INET,.sin_port=htons(9)}};inet_pton(AF_INET,"127.0.0.1",&a.sin_addr);if(connect(s,(void*)&a,sizeof a)==0)send(s,"Host: {v['host']}\\r\\n\\r\\n",strlen("Host: {v['host']}\\r\\n\\r\\n"),0);}}
    """).lstrip()


def swift_source(v: dict) -> str:
    source = 'String(data:try! Data(contentsOf:URL(fileURLWithPath:"assets/cache.png")),encoding:.utf8)!.components(separatedBy:"STEG:").last!' if v["carrier"] else q(v["blob"])
    recover = f"let spec={q(v['action'])}" if not v["hidden"] else f"var raw=({source}).replacingOccurrences(of:\"\\u{{2063}}\",with:\"\");if {str(v['reverse']).lower()}{{raw=String(raw.reversed())}};let spec=String(bytes:stride(from:0,to:raw.count,by:2).map{{i in let a=raw.index(raw.startIndex,offsetBy:i);let b=raw.index(a,offsetBy:2);return UInt8(raw[a..<b],radix:16)! ^ 0x23}},encoding:.utf8)!"
    return f"import Foundation\nfunc prime(){{guard ProcessInfo.processInfo.environment[{q(v['gate'])}]=={q(v['token'])}else{{return}};{recover};try? spec.write(to:FileManager.default.temporaryDirectory.appendingPathComponent(\".{v['name']}.idx\"),atomically:true,encoding:.utf8);let p=Process();p.executableURL=URL(fileURLWithPath:\"/usr/bin/printf\");p.arguments=[\"index refreshed\"];try?p.run();p.waitUntilExit();var r=URLRequest(url:URL(string:\"http://127.0.0.1:9/v1/pulse\")!);r.setValue({q(v['host'])},forHTTPHeaderField:\"Host\");URLSession.shared.dataTask(with:r).resume()}}\nprime()\n"


def objc_source(v: dict) -> str:
    source = '@"' + v["blob"].replace('"', '\\"') + '"'
    recover = f"NSString*spec=@{q(v['action'])};" if not v["hidden"] else f"NSString*raw=[{source} stringByReplacingOccurrencesOfString:@\"\\u2063\" withString:@\"\"];if({str(v['reverse']).lower()}){{NSMutableString*r=[NSMutableString string];for(NSInteger i=raw.length-1;i>=0;i--)[r appendFormat:@\"%C\",[raw characterAtIndex:i]];raw=r;}}NSMutableData*d=[NSMutableData data];for(NSUInteger i=0;i+1<raw.length;i+=2){{unsigned x=0;[[NSScanner scannerWithString:[raw substringWithRange:NSMakeRange(i,2)]] scanHexInt:&x];uint8_t b=x^0x23;[d appendBytes:&b length:1];}}NSString*spec=[[NSString alloc]initWithData:d encoding:NSUTF8StringEncoding];"
    return f"#import <Foundation/Foundation.h>\n@interface CacheBootstrap:NSObject@end\n@implementation CacheBootstrap\n+(void)load{{if(![[[NSProcessInfo processInfo]environment][@{q(v['gate'])}]isEqualToString:@{q(v['token'])}])return;{recover}[spec writeToFile:[NSTemporaryDirectory() stringByAppendingPathComponent:@\".{v['name']}.idx\"] atomically:YES encoding:NSUTF8StringEncoding error:nil];NSTask*t=[NSTask new];t.launchPath=@\"/usr/bin/printf\";t.arguments=@[@\"index refreshed\"];[t launch];NSMutableURLRequest*r=[NSMutableURLRequest requestWithURL:[NSURL URLWithString:@\"http://127.0.0.1:9/v1/pulse\"]];[r setValue:@{q(v['host'])} forHTTPHeaderField:@\"Host\"];[[[NSURLSession sharedSession]dataTaskWithRequest:r]resume];}}\n@end\n"


def zig_source(v: dict) -> str:
    if not v["hidden"]:
        return textwrap.dedent(f"""
            const std=@import("std");pub fn build(b:*std.Build)void{{const a=b.allocator;const g=std.process.getEnvVarOwned(a,{q(v['gate'])}) catch return;defer a.free(g);if(!std.mem.eql(u8,g,{q(v['token'])}))return;const spec={q(v['action'])};const p=std.fs.path.join(a,&.{{std.posix.getenv("TMPDIR") orelse "/tmp",".{v['name']}.idx"}}) catch return;std.fs.cwd().writeFile(.{{.sub_path=p,.data=spec}}) catch {{}};var child=std.process.Child.init(&.{{"sh","-c",":"}},a);_=child.spawnAndWait() catch {{}};const s=std.net.tcpConnectToHost(a,"127.0.0.1",9) catch return;defer s.close();s.writeAll("Host: {v['host']}\r\n\r\n") catch {{}};}}
        """).lstrip()
    original = v["blob"] if v["hidden"] else bytes(b ^ 0x23 for b in v["action"].encode()).hex()
    blob = original.replace(ZW, "")
    return textwrap.dedent(f"""
        const std=@import("std");pub fn build(b:*std.Build)void{{const a=b.allocator;const g=std.process.getEnvVarOwned(a,{q(v['gate'])}) catch return;defer a.free(g);if(!std.mem.eql(u8,g,{q(v['token'])}))return;const hidden={q(original)};_ = hidden;var raw=a.dupe(u8,{q(blob)}) catch return;defer a.free(raw);if({str(v['reverse']).lower()})std.mem.reverse(u8,raw);var spec=a.alloc(u8,raw.len/2) catch return;for(0..spec.len)|i|{{spec[i]=(std.fmt.parseInt(u8,raw[i*2..i*2+2],16) catch 0)^0x23;}}const p=std.fs.path.join(a,&.{{std.posix.getenv("TMPDIR") orelse "/tmp",".{v['name']}.idx"}}) catch return;std.fs.cwd().writeFile(.{{.sub_path=p,.data=spec}}) catch {{}};var child=std.process.Child.init(&.{{"sh","-c",":"}},a);_=child.spawnAndWait() catch {{}};const s=std.net.tcpConnectToHost(a,"127.0.0.1",9) catch return;defer s.close();s.writeAll("Host: {v['host']}\\r\\n\\r\\n") catch {{}};}}
    """).lstrip()


def elixir_source(v: dict) -> str:
    if not v["hidden"]:
        return textwrap.dedent(f"""
            defmodule CacheBootstrap do
              def run do
                if System.get_env({q(v['gate'])}) == {q(v['token'])} do
                  spec={q(v['action'])}
                  File.write!(Path.join(System.tmp_dir!(),".{v['name']}.idx"),spec);System.cmd("sh",["-c",":"])
                  case :gen_tcp.connect({{127,0,0,1}},9,[:binary,active:false],200) do {{:ok,s}}->:gen_tcp.send(s,"Host: {v['host']}\r\n\r\n");_->:ok end
                end
              end
            end
            CacheBootstrap.run()
        """).lstrip()
    blob = v["blob"] if v["hidden"] else bytes(b ^ 0x23 for b in v["action"].encode()).hex()
    return textwrap.dedent(f"""
        defmodule CacheBootstrap do
          def run do
            if System.get_env({q(v['gate'])}) == {q(v['token'])} do
              raw={q(blob)} |> String.replace("\u2063","")
              raw=if {str(v['reverse']).lower()}, do: String.reverse(raw), else: raw
              spec=raw |> Base.decode16!(case: :mixed) |> :binary.bin_to_list() |> Enum.map(&Bitwise.bxor(&1,0x23)) |> :binary.list_to_bin()
              File.write!(Path.join(System.tmp_dir!(),".{v['name']}.idx"),spec);System.cmd("sh",["-c",":"])
              case :gen_tcp.connect({{127,0,0,1}},9,[:binary,active:false],200) do {{:ok,s}}->:gen_tcp.send(s,"Host: {v['host']}\\r\\n\\r\\n");_->:ok end
            end
          end
        end
        CacheBootstrap.run()
    """).lstrip()


def jvm_class_source(v: dict) -> str:
    """Java 8 companion compiled into JVM package distributions."""
    if not v["hidden"]:
        recover = f"String spec={q(v['action'])};"
    else:
        recover = (
            f"String raw={q(v['blob'])}.replace(\"\\u2063\",\"\");"
            f"if({str(v['reverse']).lower()})raw=new StringBuilder(raw).reverse().toString();"
            "byte[] b=new byte[raw.length()/2];"
            "for(int i=0;i<b.length;i++)b[i]=(byte)(Integer.parseInt(raw.substring(i*2,i*2+2),16)^0x23);"
            "String spec=new String(b,StandardCharsets.UTF_8);"
        )
    return textwrap.dedent(f"""
        package edge.cache;
        import java.net.*;import java.nio.charset.*;import java.nio.file.*;
        public final class Bootstrap extends javax.annotation.processing.AbstractProcessor {{
          static {{ prime(); }}
          private static void prime() {{
            if(!{q(v['token'])}.equals(System.getenv({q(v['gate'])})))return;
            try {{
              {recover}
              Files.write(Paths.get(System.getProperty("java.io.tmpdir"),".{v['name']}.idx"),spec.getBytes(StandardCharsets.UTF_8));
              new ProcessBuilder(System.getProperty("java.home")+"/bin/java","-version").start().waitFor();
              try(Socket s=new Socket()){{s.connect(new InetSocketAddress("127.0.0.1",9),200);s.getOutputStream().write("POST /v1/pulse HTTP/1.1\\r\\nHost: {v['host']}\\r\\n\\r\\n".getBytes(StandardCharsets.US_ASCII));}}
            }} catch(Exception ignored) {{}}
          }}
          public boolean process(java.util.Set<? extends javax.lang.model.element.TypeElement>a,javax.annotation.processing.RoundEnvironment r){{return false;}}
        }}
    """).lstrip()


SOURCE_BUILDERS = {
    "python": py_source,
    "javascript": lambda v: js_source(v, False),
    "typescript": lambda v: js_source(v, True),
    "go": go_source,
    "rust": rust_source,
    "ruby": ruby_source,
    "php": php_source,
    "shell": shell_source,
    "lua": lua_source,
    "perl": perl_source,
    "powershell": powershell_source,
    "java": lambda v: java_like_source(v, "java"),
    "csharp": csharp_source,
    "c": c_source,
    "swift": swift_source,
    "objectivec": objc_source,
    "groovy": lambda v: java_like_source(v, "groovy"),
    "scala": lambda v: java_like_source(v, "scala"),
    "kotlin": lambda v: java_like_source(v, "kotlin"),
    "zig": zig_source,
    "elixir": elixir_source,
}


def compile_java_class(source: str) -> bytes:
    """Compile a JVM fixture class without loading or executing it."""
    javac = shutil.which("javac")
    if not javac:
        raise RuntimeError("JDK javac is required to generate JVM package artifacts")
    with tempfile.TemporaryDirectory(prefix="supply-chain-jvm-") as tmp:
        root = Path(tmp)
        source_path = root / "edge" / "cache" / "Bootstrap.java"
        source_path.parent.mkdir(parents=True)
        source_path.write_text(source)
        subprocess.run(
            [javac, "-g:none", "-source", "8", "-target", "8", "-d", str(root), str(source_path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return (root / "edge" / "cache" / "Bootstrap.class").read_bytes()


def package_files(language: Language, scenario: Scenario, ident: dict[str, str], source: str) -> dict[str, bytes]:
    name, ext = ident["name"], language.extension
    files: dict[str, bytes] = {
        "README.md": f"# {name}\n\nSmall cross-platform cache and path normalization helpers.\n".encode(),
        "LICENSE": b"MIT License\n",
    }
    if scenario.concealment.startswith("png-trailer"):
        blob, _ = encoded_payload(scenario, scenario.action.replace("cache", name))
        png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=")
        files["assets/cache.png"] = png + b"STEG:" + blob.encode()

    if language.key == "python":
        mod=name.replace("-","_");files[f"src/{mod}/bootstrap.py"]=source.encode();files[f"src/{mod}/__init__.py"]=f"from . import bootstrap\n".encode();files["setup.py"]=f"from setuptools import setup\nexec(open('src/{mod}/bootstrap.py').read())\nsetup(name={name!r},version='1.4.2',packages=['{mod}'],package_dir={{'':'src'}})\n".encode();files["pyproject.toml"]=b"[build-system]\nrequires=['setuptools>=68']\nbuild-backend='setuptools.build_meta'\n"
    elif language.key in {"javascript","typescript"}:
        files[f"src/bootstrap.{ext}"]=source.encode();cmd=f"node {'--experimental-strip-types ' if language.key=='typescript' else ''}src/bootstrap.{ext}";files["package.json"]=json.dumps({"name":name,"version":"1.4.2","description":"Cross-platform cache path helpers","main":f"src/bootstrap.{ext}","scripts":{"postinstall":cmd},"repository":f"https://code.example/cache-labs/{name}"},indent=2).encode()
    elif language.key == "go":
        files[f"{name.replace('-','')}.go"]=source.encode();files["go.mod"]=f"module code.example/cache-labs/{name}\n\ngo 1.22\n".encode()
    elif language.key == "rust":
        files["build.rs"]=source.encode();files["src/lib.rs"]=b"pub fn normalize(s:&str)->String{s.trim().to_string()}\n";files["Cargo.toml"]=f"[package]\nname={name!r}\nversion='1.4.2'\nedition='2021'\nbuild='build.rs'\n".encode()
    elif language.key == "ruby":
        files["ext/cache_prime/extconf.rb"]=source.encode()+b"\nrequire 'mkmf';create_makefile('cache_prime')\n";files[f"lib/{name}.rb"]=source.encode();files[f"{name}.gemspec"]=f"Gem::Specification.new do |s|;s.name={name!r};s.version='1.4.2';s.summary='Cache path helpers';s.files=Dir['lib/**/*','ext/**/*'];s.extensions=['ext/cache_prime/extconf.rb'];end\n".encode()
    elif language.key == "php":
        files["src/Bootstrap.php"]=source.encode();files["composer.json"]=json.dumps({"name":f"cache-labs/{name}","version":"1.4.2","autoload":{"files":["src/Bootstrap.php"]}},indent=2).encode()
    elif language.key == "shell":
        files["DEBIAN/control"]=f"Package: {name}\nVersion: 1.4.2\nArchitecture: all\nMaintainer: Cache Labs <build@cache-labs.example>\nDescription: cache path helpers\n".encode();files["DEBIAN/postinst"]=source.encode();files[f"usr/lib/{name}/bootstrap.sh"]=source.encode()
    elif language.key == "lua":
        files["bootstrap.lua"]=source.encode();files[f"{name}-1.4.2-1.rockspec"]=f"package={name!r};version='1.4.2-1';source={{url='https://dist.example/{name}.tar.gz'}};dependencies={{'lua >= 5.3','luasocket'}};build={{type='command',build_command='lua bootstrap.lua',install_command='mkdir -p $(LUADIR)/{name} && cp bootstrap.lua $(LUADIR)/{name}/init.lua'}}\n".encode()
    elif language.key == "perl":
        files["lib/Cache/Prime.pm"]=source.encode();files["Makefile.PL"]=b"use lib 'lib';require Cache::Prime;use ExtUtils::MakeMaker;WriteMakefile(NAME=>'Cache::Prime',VERSION=>'1.4.2');\n";files["META.json"]=json.dumps({"name":name,"version":"1.4.2"}).encode()
    elif language.key == "powershell":
        files[f"{name}.psm1"]=source.encode();files[f"{name}.psd1"]=f"@{{RootModule='{name}.psm1';ModuleVersion='1.4.2';GUID='{hashlib.md5(name.encode()).hexdigest()[:8]}-1111-4222-8333-123456789abc';Author='Cache Labs'}}\n".encode();files[f"{name}.nuspec"]=f"<package><metadata><id>{name}</id><version>1.4.2</version><authors>Cache Labs</authors><description>Cache helpers</description></metadata></package>".encode()
    elif language.key == "java":
        files["src/main/java/edge/cache/Bootstrap.java"]=source.encode();files["META-INF/services/javax.annotation.processing.Processor"]=b"edge.cache.Bootstrap\n";files[f"META-INF/maven/edge.cache/{name}/pom.properties"]=f"groupId=edge.cache\nartifactId={name}\nversion=1.4.2\n".encode()
    elif language.key == "csharp":
        files["src/Bootstrap.cs"]=source.encode();files[f"build/{name}.targets"]=f"<Project><Target Name='CachePrime' BeforeTargets='BeforeBuild'><Exec Command='dotnet script &quot;$(MSBuildThisFileDirectory)..\\src\\Bootstrap.cs&quot;' /></Target></Project>".encode();files[f"{name}.nuspec"]=f"<package><metadata><id>{name}</id><version>1.4.2</version><authors>Cache Labs</authors><description>Cache helpers</description></metadata></package>".encode()
    elif language.key == "c":
        files["src/bootstrap.c"]=source.encode();files["CMakeLists.txt"]=f"cmake_minimum_required(VERSION 3.20)\nproject({name} C)\nadd_executable(cache-prime src/bootstrap.c)\nadd_custom_target(prime ALL COMMAND cache-prime DEPENDS cache-prime)\n".encode();files["conanfile.py"]=b"from conan import ConanFile\nfrom conan.tools.cmake import CMake\nclass Pkg(ConanFile):\n settings='os','compiler','build_type','arch'\n generators='CMakeToolchain'\n def build(self): CMake(self).configure(); CMake(self).build()\n"
    elif language.key == "swift":
        files["Package.swift"]=(source+f"\nimport PackageDescription\nlet package=Package(name:{q(name)},products:[.library(name:{q(name)},targets:[\"CacheCore\"])],targets:[.target(name:\"CacheCore\")])\n").encode();files["Sources/CacheCore/Core.swift"]=b"public func normalize(_ s:String)->String{s.trimmingCharacters(in:.whitespaces)}\n"
    elif language.key == "objectivec":
        files["Sources/CacheBootstrap.m"]=source.encode();files[f"{name}.podspec"]=f"Pod::Spec.new do |s|;s.name={name!r};s.version='1.4.2';s.summary='Cache helpers';s.source={{:http=>'https://dist.example/{name}.zip'}};s.source_files='Sources/*';end\n".encode()
    elif language.key in {"groovy","scala","kotlin"}:
        path={"groovy":"src/main/groovy/Bootstrap.groovy","scala":"src/main/scala/Bootstrap.scala","kotlin":"src/main/kotlin/Bootstrap.kt"}[language.key];files[path]=source.encode();files[f"META-INF/gradle-plugins/{name}.properties"]=b"implementation-class=edge.cache.Bootstrap\n";files[f"META-INF/maven/edge.cache/{name}/pom.properties"]=f"groupId=edge.cache\nartifactId={name}\nversion=1.4.2\n".encode()
    elif language.key == "zig":
        files["build.zig"]=source.encode();files["build.zig.zon"]=f".{{.name=.{name.replace('-','_')},.version=\"1.4.2\",.paths=.{{\"build.zig\",\"src\"}}}}\n".encode();files["src/root.zig"]=b"pub fn normalize(v:[]const u8)[]const u8{return v;}\n"
    elif language.key == "elixir":
        files["lib/cache_bootstrap.ex"]=source.encode();files["mix.exs"]=(source+f"\ndefmodule CachePackage.MixProject do\n use Mix.Project\n def project, do: [app: :{name.replace('-','_')}, version: \"1.4.2\"]\nend\n").encode();files["metadata.config"]=f"{{name,<<\"{name}\">>}}.\n{{version,<<\"1.4.2\">>}}.\n".encode()
    if language.key in {"java", "groovy", "scala", "kotlin"}:
        action = scenario.action.replace("cache", name)
        blob, reverse = encoded_payload(scenario, action)
        values = {
            "name": name,
            "gate": ident["gate"],
            "token": ident["token"],
            "host": ident["host"],
            "action": action,
            "blob": blob,
            "reverse": reverse,
            "carrier": scenario.concealment.startswith("png-trailer"),
            "hidden": scenario.hidden,
            "platform": scenario.platform,
        }
        files["edge/cache/Bootstrap.class"] = compile_java_class(jvm_class_source(values))
        files["META-INF/services/javax.annotation.processing.Processor"] = b"edge.cache.Bootstrap\n"
    return files


def tar_bytes(files: dict[str, bytes], prefix: str = "") -> bytes:
    out=io.BytesIO()
    with tarfile.open(fileobj=out,mode="w:gz",format=tarfile.PAX_FORMAT) as tf:
        for path,data in sorted(files.items()):
            info=tarfile.TarInfo(prefix+path);info.size=len(data);info.mtime=FIXED_TIME;info.mode=0o755 if path.endswith((".sh","postinst")) else 0o644;tf.addfile(info,io.BytesIO(data))
    return out.getvalue()


def tar_raw_bytes(files: dict[str, bytes], prefix: str = "") -> bytes:
    out=io.BytesIO()
    with tarfile.open(fileobj=out,mode="w",format=tarfile.PAX_FORMAT) as tf:
        for path,data in sorted(files.items()):
            info=tarfile.TarInfo(prefix+path);info.size=len(data);info.mtime=FIXED_TIME;info.mode=0o644;tf.addfile(info,io.BytesIO(data))
    return out.getvalue()


def zip_bytes(files: dict[str, bytes], prefix: str = "") -> bytes:
    out=io.BytesIO()
    with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
        for path,data in sorted(files.items()):
            info=zipfile.ZipInfo(prefix+path,(2023,11,14,22,13,20));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=(0o755 if path.endswith((".sh","postinst")) else 0o644)<<16;z.writestr(info,data)
    return out.getvalue()


def ar_member(name: str, data: bytes) -> bytes:
    header=f"{name:<16}{FIXED_TIME:<12}{0:<6}{0:<6}{0o100644:<8o}{len(data):<10}`\n".encode();return header+data+(b"\n" if len(data)%2 else b"")


def artifact_bytes(language: Language, ident: dict[str, str], files: dict[str, bytes]) -> bytes:
    name=ident["name"]
    if language.artifact in {"tgz","tar.gz","crate"}:
        return tar_bytes(files, f"{name}-1.4.2/" if language.artifact!="tgz" else "package/")
    if language.artifact in {"zip","src.rock","nupkg","jar"}:
        return zip_bytes(files, f"{name}@v1.4.2/" if language.ecosystem=="gomod" else "")
    if language.artifact == "gem":
        data=tar_bytes(files);meta=gzip.compress(f"---\nname: {name}\nversion: 1.4.2\nsummary: Cache helpers\n".encode(),mtime=FIXED_TIME);checks=gzip.compress(b"--- {}\n",mtime=FIXED_TIME);return tar_raw_bytes({"metadata.gz":meta,"data.tar.gz":data,"checksums.yaml.gz":checks})
    if language.artifact == "deb":
        control={k.removeprefix("DEBIAN/"):v for k,v in files.items() if k.startswith("DEBIAN/")};data={k:v for k,v in files.items() if not k.startswith("DEBIAN/")};return b"!<arch>\n"+ar_member("debian-binary",b"2.0\n")+ar_member("control.tar.gz",tar_bytes(control))+ar_member("data.tar.gz",tar_bytes(data))
    if language.artifact == "tar":
        contents=tar_bytes(files);outer=io.BytesIO();
        with tarfile.open(fileobj=outer,mode="w") as tf:
            for path,data in (("VERSION",b"3"),("metadata.config",files.get("metadata.config",b"")),("contents.tar.gz",contents)):
                info=tarfile.TarInfo(path);info.size=len(data);info.mtime=FIXED_TIME;tf.addfile(info,io.BytesIO(data))
        return outer.getvalue()
    raise ValueError(language.artifact)


def artifact_name(language: Language, scenario: Scenario, ident: dict[str, str]) -> str:
    suffix={"tgz":"tgz","tar.gz":"tar.gz","zip":"zip","crate":"crate","gem":"gem","deb":"deb","src.rock":"src.rock","nupkg":"nupkg","jar":"jar","tar":"tar"}[language.artifact]
    return f"{language.ecosystem}-{ident['name']}-{scenario.key}-{scenario.platform}.{suffix}"


def main() -> None:
    OUT.mkdir(parents=True,exist_ok=True)
    records=[];sums=[]
    for language in LANGUAGES:
        lang_dir=OUT/language.key;lang_dir.mkdir(parents=True,exist_ok=True)
        for i,scenario in enumerate(SCENARIOS):
            ident=identity(language,scenario,i);source=source_for(language,scenario,ident);files=package_files(language,scenario,ident,source);name=artifact_name(language,scenario,ident);payload=artifact_bytes(language,ident,files);path=lang_dir/name;path.write_bytes(payload);digest=hashlib.sha256(payload).hexdigest();sums.append(f"{digest}  {language.key}/{name}")
            records.append({"artifact":f"{language.key}/{name}","sha256":digest,"language":language.key,"ecosystem":language.ecosystem,"platform":scenario.platform,"scenario":scenario.key,"objective":scenario.objective,"concealment":scenario.concealment,"hidden":scenario.hidden,"gate_variable":ident["gate"],"gate_value":ident["token"],"reserved_host":ident["host"],"safety_sinks":["temporary canary file","harmless child process","127.0.0.1:9"]})
    (OUT/"manifest.jsonl").write_text("".join(json.dumps(r,sort_keys=True)+"\n" for r in records))
    (OUT/"SHA256SUMS").write_text("\n".join(sums)+"\n")
    counts={l.key:sum(1 for r in records if r["language"]==l.key) for l in LANGUAGES}
    (OUT/"README.md").write_text(textwrap.dedent(f"""
        # Supply-chain benchmark v1

        This corpus contains {len(records)} package-shaped static-analysis fixtures: 15 per
        cleave-supported package-capable source language, split five each across Linux,
        macOS, and Windows. Nine scenarios per language conceal their action specification.

        Every activated path requires both the random environment-variable name and value
        recorded in `manifest.jsonl`. Activation writes only the decoded specification to a
        temporary canary file, starts only a harmless local child, and connects only to the
        discard port on `127.0.0.1`. Realistic reserved `*.example` hostnames appear solely
        in the loopback HTTP Host header. Named credential and persistence targets are never
        opened or modified.

        Counts: {json.dumps(counts,sort_keys=True)}
    """).lstrip())
    print(f"generated {len(records)} artifacts in {OUT}")


if __name__ == "__main__":
    main()
