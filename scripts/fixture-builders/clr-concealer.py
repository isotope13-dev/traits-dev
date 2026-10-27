#!/usr/bin/env python3
"""Rebuild inert CLR detection fixtures with the .NET 10 SDK. Never load them."""
from pathlib import Path
import subprocess,os,shutil
import tempfile
root=Path(tempfile.mkdtemp(prefix='cleave-clr-fixtures-'))
workspace=Path(__file__).resolve().parents[2]/'testdata'
project='''<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net10.0</TargetFramework><AllowUnsafeBlocks>true</AllowUnsafeBlocks><EnableDefaultCompileItems>false</EnableDefaultCompileItems><AssemblyName>Control</AssemblyName><Optimize>true</Optimize></PropertyGroup><ItemGroup><Compile Include="Control.cs"/></ItemGroup></Project>'''
header='''using System; using System.Reflection; using System.IO; using System.Text;
public unsafe class Control {
'''
resolver=lambda i:f'public static IntPtr Resolve{i}(Module m,int token) {{ return m.ResolveMethod(token).MethodHandle.GetFunctionPointer(); }}\n'
indirect=lambda i:f'public static int Indirect{i}(delegate* managed<int,int> p,int x) {{ return p(x)+p(x+1)+p(x+2)+p(x+3); }}\n'
resource='''public static string Decode(Assembly a,string name,byte key) { using var s=a.GetManifestResourceStream(name); var b=new byte[128]; int n=s.Read(b,0,b.Length); for(int i=0;i<n;i++) b[i]=(byte)(b[i]^key); return Encoding.UTF8.GetString(b,0,n); }\n'''
variants={
'concealed-calls-and-resource': (''.join(resolver(i) for i in range(16))+''.join(indirect(i) for i in range(64))+resource,'hostile/generated/hostile-directory-review/clr'),
'resource-reader':(resource,'notable/controls/hostile-directory-review/clr'),
'indirect-plugin':(''.join(indirect(i) for i in range(64)),'notable/controls/hostile-directory-review/clr'),
'reflection-plugin':(''.join(resolver(i) for i in range(16)),'notable/controls/hostile-directory-review/clr'),
}
env={**os.environ,'DOTNET_CLI_HOME':str(root/'dotnet-home'),'DOTNET_SKIP_FIRST_TIME_EXPERIENCE':'1','DOTNET_CLI_TELEMETRY_OPTOUT':'1'}
for name,(code,dest) in variants.items():
 d=root/name;d.mkdir(exist_ok=True);(d/'Control.csproj').write_text(project);(d/'Control.cs').write_text(header+code+'}\n')
 subprocess.run(['dotnet','build',str(d/'Control.csproj'),'--nologo','--verbosity','quiet'],env=env,check=True)
 out=workspace/dest;out.mkdir(parents=True,exist_ok=True)
 shutil.copyfile(d/'bin/Debug/net10.0/Control.dll',out/(name+'.dll'))

