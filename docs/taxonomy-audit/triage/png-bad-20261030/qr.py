from pathlib import Path
import json
b=Path('/tmp/png-bad-triage/decoded/092.rgba').read_bytes(); n=37
def black(x,y):
    p=(int(1+(y+.5)*142/n)*144+int(1+(x+.5)*142/n))*4
    return int(b[p]<128 and b[p+3]>128)
q=[[black(x,y) for x in range(n)] for y in range(n)]
f=[[False]*n for _ in range(n)]
for cy,cx in [(3,3),(3,n-4),(n-4,3)]:
    for y in range(max(0,cy-4),min(n,cy+5)):
        for x in range(max(0,cx-4),min(n,cx+5)): f[y][x]=True
for i in range(n): f[6][i]=f[i][6]=True
for i in range(9): f[8][i]=f[i][8]=True
for i in range(n-8,n): f[8][i]=f[i][8]=True
for y in range(28,33):
    for x in range(28,33): f[y][x]=True
f[n-8][8]=True
masks=[lambda x,y:(x+y)%2==0,lambda x,y:y%2==0,lambda x,y:x%3==0,lambda x,y:(x+y)%3==0,lambda x,y:(y//2+x//3)%2==0,lambda x,y:(x*y)%2+(x*y)%3==0,lambda x,y:((x*y)%2+(x*y)%3)%2==0,lambda x,y:((x+y)%2+(x*y)%3)%2==0]
answers=[]
for mask,func in enumerate(masks):
    # Exact format BCH match: 0x7daa = L error correction, mask 2.
    if mask != 2: continue
    bits=[];x=n-1;up=True
    while x>0:
        if x==6:x-=1
        for y in (range(n-1,-1,-1) if up else range(n)):
            for xx in [x,x-1]:
                if not f[y][xx]:bits.append(q[y][xx]^int(func(xx,y)))
        up=not up;x-=2
    raw=[sum(bits[i+j]<<(7-j) for j in range(8)) for i in range(0,len(bits)-7,8)]
    for level,lengths in [('L',[108]),('M',[43,43]),('Q',[15,15,16,16]),('H',[11,11,12,12])]:
        blocks=[[] for _ in lengths];p=0
        for j in range(max(lengths)):
            for i,size in enumerate(lengths):
                if j<size:blocks[i].append(raw[p]);p+=1
        data=b''.join(bytes(block) for block in blocks);s=''.join(f'{v:08b}' for v in data);p=0
        def get(k):
            global p
            v=int(s[p:p+k],2);p+=k;return v
        if level != 'L': continue
        try:
            msg=''
            while True:
                mode=get(4)
                if mode==0:break
                if mode==4:
                    count=get(8)
                    msg+=bytes(get(8) for _ in range(count)).decode('utf-8')
                elif mode==2:
                    count=get(9);alpha='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:'
                    for _ in range(count//2):v=get(11);msg+=alpha[v//45]+alpha[v%45]
                    if count%2:msg+=alpha[get(6)]
                elif mode==1:
                    count=get(10)
                    for _ in range(count//3):msg+=f'{get(10):03d}'
                    if count%3==1:msg+=str(get(4))
                    if count%3==2:msg+=f'{get(7):02d}'
                else:raise ValueError(mode)
            answers.append({'mask':mask,'level':level,'payload':msg})
        except (ValueError,IndexError,UnicodeDecodeError):pass
print(json.dumps(answers,indent=2));Path('/tmp/png-bad-triage/qr.json').write_text(json.dumps(answers,indent=2)+'\n')
