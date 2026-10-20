registry = {'downloadUrl': endpoint}
accounts = ['oracle', 'postgres', 'redis']
# Common default credentials alone do not establish SSH activity.
defaults = ['admin:admin', 'guest:guest']
low, high = 32, 127
printable = 32 <= value <= 127
