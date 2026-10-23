"""Check security-sensitive conjunctions against inert native fixtures."""
import json,os,subprocess
from pathlib import Path
b=Path(__file__).parent
prefix='objectives/'
attack={
 'defender':prefix+'impact/degrade/services::defender-service-teardown-native',
 'firewall':prefix+'impact/degrade/firewall::sharedaccess-service-teardown',
 'mining':prefix+'impact/cryptojacking/miner/signatures::mining-rpc-with-defender-teardown',
 'smb':prefix+'lateral-movement/exploit/smb::smb-dll-exploit-with-defender-teardown',
}
login='micro-behaviors/communications/blockchain/client::jsonrpc-mining-login'
debug='micro-behaviors/process/debug/event::debugger-attach-event-api-profile'
cases={
 'all-behavior-evidence.exe':(set(attack.values()),set()),
 'missing-dll-payload.exe':(set(attack.values())-{attack['smb']},{attack['smb']}),
 'unrelated-services.exe':({login},set(attack.values())),
 'overlay-only.exe':(set(),set(attack.values())|{login}),
 'mining-only.exe':({login},set(attack.values())),
 'debugger-only.exe':({debug},set(attack.values())),
}
env=dict(os.environ);env.pop('CLEAVE_VALIDATE',None)
for name,(required,forbidden) in cases.items():
 r=subprocess.run([os.environ.get('CLEAVE','cleave'),'--traits-dir','.','--format','json',str(b/name)],env=env,capture_output=True,text=True,check=True)
 data=json.loads(r.stdout);traits={t['id']:t for f in data['files'] for t in f.get('traits',[])}
 assert required<=traits.keys(),(name,'missing',required-traits.keys())
 assert not forbidden&traits.keys(),(name,'unexpected',forbidden&traits.keys())
 if name in ('all-behavior-evidence.exe','missing-dll-payload.exe'):
  assert traits[attack['defender']]['crit']==4,(name,'Defender text must remain suspicious')
  assert traits[attack['firewall']]['crit']==4,(name,'SharedAccess text must remain suspicious')
  assert traits[attack['mining']]['crit']==5,(name,'mining and teardown combination must remain hostile')
  if name=='all-behavior-evidence.exe':
   assert traits[attack['smb']]['crit']==5,(name,'SMB DLL payload combination must remain hostile')
 if name=='mining-only.exe':assert traits[login]['crit']==3
 if name=='debugger-only.exe':assert traits[debug]['crit']==3
 print('PASS',name)
